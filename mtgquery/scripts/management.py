from sqlalchemy import create_engine
from ..models import (
    DBSession,
    Base,
)
import os

sqlalchemy_url = os.environ.get('DATABASE_URL')
engine = create_engine(sqlalchemy_url)
engine.execute("select 1").scalar()
DBSession.configure(bind=engine)
Base.metadata.bind = engine
