from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Ufile(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    class_name = Column(String)
    week_name = Column(String)
    file_name = Column(String)
    size = Column(Integer)
    date = Column(String)
    type = Column(String)
    user_id = Column(Integer)
    path = Column(String)


class Files():
    def __init__(self):
        # Connect to the database
        engine = create_engine('sqlite:///example2.db')

        # Create the tables
        Base.metadata.create_all(engine)

        # Create a session
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_file(self, name, class_name, week_name, file_name, size, date, type, user_id, path):
        self.session.add(Ufile(name=name, class_name=class_name, week_name=week_name, file_name=file_name, size=size, date=date, type=type, user_id=user_id, path=path))
        self.session.commit()

    def get_file_path(self,class_name,week_name,file_name):
        file = self.session.query(Ufile).filter_by(class_name=class_name, week_name=week_name, file_name=file_name).first()
        return file.path
    #this function looks in the database, and get a list of all the classes
    def get_classes_list(self):
        classes = self.session.query(Ufile.class_name).distinct().all()
        classes = [i[0] for i in classes]
        return classes
    def get_weeks_list(self, class_name):
        weeks = self.session.query(Ufile.week_name).filter_by(class_name=class_name).distinct().all()
        weeks = [i[0] for i in weeks]
        return weeks

    def get_files_list(self, class_name, week_name):
        files = self.session.query(Ufile.file_name).filter_by(class_name=class_name, week_name=week_name).all()
        files = [i[0] for i in files]
        return files






if __name__ == '__main__':
    f = Files() 
    f.add_file('hw1', 'cs61a', 'week1', 'hw1.py', 100, '2019-01-01', 'python', 1, '/home/cs61a/hw1.py')
    print(f.get_file_path('cs61a', 'week1', 'hw1.py'))
    print(f.get_classes_list())
    print(f.get_weeks_list('cs61a'))
    print(f.get_files_list('cs61a', 'week1'))