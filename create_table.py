from database import Base, engine
import models  # make sure all your models are imported here

Base.metadata.create_all(bind=engine)

print("Tables created successfully in PostgreSQL!")