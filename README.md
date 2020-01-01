
In the env.py file that get after run alembic -c development.ini init alembic, update like:

# add your model's MetaData object here
# for 'autogenerate' support
from pyratest.models.meta import Base
target_metadata = Base.metadata

alembic -c development.ini revision --autogenerate -m "some message"   and upgrade head

