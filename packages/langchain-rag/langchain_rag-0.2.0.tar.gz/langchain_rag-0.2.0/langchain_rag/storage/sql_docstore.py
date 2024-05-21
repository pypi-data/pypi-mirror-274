import contextlib
from pathlib import Path
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterator,
    Dict,
    Generator,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from langchain_core.stores import BaseStore, V
from sqlalchemy import (
    Column,
    Engine,
    PickleType,
    and_,
    create_engine,
    delete,
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    Mapped,
    Session,
    declarative_base,
    mapped_column,
    sessionmaker,
)

Base = declarative_base()


def items_equal(x: Any, y: Any) -> bool:
    return x == y


class Value(Base):  # type: ignore[valid-type,misc]
    """Table used to save values."""

    # ATTENTION:
    # Prior to modifying this table, please determine whether
    # we should create migrations for this table to make sure
    # users do not experience data loss.
    __tablename__ = "docstore"

    namespace: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=False)
    key: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=False)
    # value: Mapped[Any] = Column(type_=PickleType, index=False, nullable=False)
    value: Any = Column("earthquake", PickleType(comparator=items_equal))


# This is a fix of original SQLStore.
# This can will be removed when a PR will be merged.
class SQLStore(BaseStore[str, bytes]):
    """BaseStore interface that works on an SQL database.

    Examples:
        Create a SQLStore instance and perform operations on it:

        .. code-block:: python

            from langchain_rag.storage import SQLStore

            # Instantiate the SQLStore with the root path
            sql_store = SQLStore(namespace="test", db_url="sqllite://:memory:")

            # Set values for keys
            sql_store.mset([("key1", b"value1"), ("key2", b"value2")])

            # Get values for keys
            values = sql_store.mget(["key1", "key2"])  # Returns [b"value1", b"value2"]

            # Delete keys
            sql_store.mdelete(["key1"])

            # Iterate over keys
            for key in sql_store.yield_keys():
                print(key)

    """

    def __init__(
        self,
        *,
        namespace: str,
        db_url: Optional[Union[str, Path]] = None,
        engine: Optional[Union[Engine, AsyncEngine]] = None,
        engine_kwargs: Optional[Dict[str, Any]] = None,
        async_mode: bool = False,
    ):
        if db_url is None and engine is None:
            raise ValueError("Must specify either db_url or engine")

        if db_url is not None and engine is not None:
            raise ValueError("Must specify either db_url or engine, not both")

        _engine: Union[Engine, AsyncEngine]
        if db_url:
            if async_mode:
                _engine = create_async_engine(
                    url=str(db_url),
                    **(engine_kwargs or {}),
                )
            else:
                _engine = create_engine(url=str(db_url), **(engine_kwargs or {}))
        elif engine:
            _engine = engine

        else:
            raise AssertionError("Something went wrong with configuration of engine.")

        _session_factory: Union[sessionmaker[Session], async_sessionmaker[AsyncSession]]
        if isinstance(_engine, AsyncEngine):
            _session_factory = async_sessionmaker(bind=_engine)
        else:
            _session_factory = sessionmaker(bind=_engine)

        self.engine = _engine
        self.dialect = _engine.dialect.name
        self.session_factory = _session_factory
        self.namespace = namespace

    def create_schema(self) -> None:
        Base.metadata.create_all(self.engine)

    async def acreate_schema(self) -> None:
        assert isinstance(self.engine, AsyncEngine)
        async with self.engine.begin() as session:
            await session.run_sync(Base.metadata.create_all)

    def drop(self) -> None:
        Base.metadata.drop_all(bind=self.engine.connect())

    async def amget(self, keys: Sequence[str]) -> List[Optional[V]]:
        assert isinstance(self.engine, AsyncEngine)
        result: Dict[str, V] = {}
        async with self._amake_session() as session:
            stmt = select(Value).filter(
                and_(
                    Value.key.in_(keys),
                    Value.namespace == self.namespace,
                )
            )
            for v in await session.scalars(stmt):
                result[v.key] = v.value
        return [result.get(key) for key in keys]

    def mget(self, keys: Sequence[str]) -> List[Optional[bytes]]:
        result = {}

        with self._make_session() as session:
            stmt = select(Value).filter(
                and_(
                    Value.key.in_(keys),
                    Value.namespace == self.namespace,
                )
            )
            for v in session.scalars(stmt):
                result[v.key] = v.value
        return [result.get(key) for key in keys]

    async def amset(self, key_value_pairs: Sequence[Tuple[str, V]]) -> None:
        async with self._amake_session() as session:
            await self._amdelete([key for key, _ in key_value_pairs], session)
            session.add_all(
                [
                    Value(namespace=self.namespace, key=k, value=v)
                    for k, v in key_value_pairs
                ]
            )
            await session.commit()

    def mset(self, key_value_pairs: Sequence[Tuple[str, bytes]]) -> None:
        values: Dict[str, bytes] = dict(key_value_pairs)
        with self._make_session() as session:
            self._mdelete(list(values.keys()), session)
            session.add_all(
                [
                    Value(namespace=self.namespace, key=k, value=v)
                    for k, v in values.items()
                ]
            )
            session.commit()

    def _mdelete(self, keys: Sequence[str], session: Session) -> None:
        stmt = delete(Value).filter(
            and_(
                Value.key.in_(keys),
                Value.namespace == self.namespace,
            )
        )
        session.execute(stmt)

    async def _amdelete(self, keys: Sequence[str], session: AsyncSession) -> None:
        stmt = delete(Value).filter(
            and_(
                Value.key.in_(keys),
                Value.namespace == self.namespace,
            )
        )
        await session.execute(stmt)

    def mdelete(self, keys: Sequence[str]) -> None:
        with self._make_session() as session:
            self._mdelete(keys, session)
            session.commit()

    async def amdelete(self, keys: Sequence[str]) -> None:
        async with self._amake_session() as session:
            await self._amdelete(keys, session)
            await session.commit()

    def yield_keys(self, *, prefix: Optional[str] = None) -> Iterator[str]:
        with self._make_session() as session:
            for v in session.query(Value).filter(  # type: ignore
                Value.namespace == self.namespace
            ):
                yield str(v.key)
            session.close()

    async def ayield_keys(self, *, prefix: Optional[str] = None) -> AsyncIterator[str]:
        async with self._amake_session() as session:
            stmt = select(Value).filter(Value.namespace == self.namespace)
            for v in await session.scalars(stmt):
                yield str(v.key)
            await session.close()

    @contextlib.contextmanager
    def _make_session(self) -> Generator[Session, None, None]:
        """Create a session and close it after use."""

        if isinstance(self.session_factory, async_sessionmaker | async_scoped_session):
            raise AssertionError("This method is not supported for async engines.")

        yield self.session_factory()

    @contextlib.asynccontextmanager
    async def _amake_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Create a session and close it after use."""

        if not isinstance(
            self.session_factory, async_sessionmaker | async_scoped_session
        ):
            raise AssertionError("This method is not supported for sync engines.")

        async with self.session_factory() as session:
            yield session
