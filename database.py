from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime









Base = declarative_base()
#this configures all the fields that are in the database
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

#the main class you will be interacting with
class Files():
    def __init__(self):
        # Connect to the database
        engine = create_engine('sqlite:///main.db')

        # Create the tables
        Base.metadata.create_all(engine)

        # Create a session
        Session = sessionmaker(bind=engine)
        self.session = Session()

    #adds a file to the database. It takes the file info as arguments, and puts them as columns in the database
    def add_file(self, name, class_name, week_name, file_name, path, user_id=1):
        self.session.add(Ufile(name=name, class_name=class_name, week_name=week_name, file_name=file_name, date=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), type=file_name[file_name.rindex(".")+1:len(file_name)], path=path, user_id=user_id,))
        self.session.commit()

    #gets the gives you the file path when you give it the class name, week name, and note name
    def get_file_path(self,class_name,week_name,file_name):
        file = self.session.query(Ufile).filter_by(class_name=class_name, week_name=week_name, file_name=file_name).first()
        return file.path
   
    #this function looks in the database, and get a list of all the classes
    def get_classes_list(self):
        classes = self.session.query(Ufile.class_name).distinct().all()
        classes = [i[0] for i in classes]
        return classes
    
    #this function looks in the database, and get a list of all the weeks in the specified class
    def get_weeks_list(self, class_name):
        weeks = self.session.query(Ufile.week_name).filter_by(class_name=class_name).distinct().all()
        weeks = [i[0] for i in weeks]
        return weeks

    #this function looks in the database, and get a list of all the files in the specified class and week
    def get_files_list(self, class_name, week_name):
        files = self.session.query(Ufile.file_name).filter_by(class_name=class_name, week_name=week_name).all()
        files = [i[0] for i in files]
        return files
    def delete_file(self, class_name, week_name, file_name):
        file_to_delete = self.session.query(Ufile).filter_by(class_name=class_name, week_name=week_name, file_name=file_name).first()
        self.session.delete(file_to_delete)
        self.session.commit()







class Class(Base):
    #id so that we can delete or modify a specific element. Primary key generates this unique id
    __tablename__ = 'class'
    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable=False)
    date_added = Column(String, default=str(datetime.datetime.now))

    def __repr__(self):
        return '<Name %r>' % self.name

class folder(Base):
    #id so that we can delete or modify a specific element. Primary key generates this unique id
    __tablename__ = 'folder'
    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable=False)
    date_added = Column(String, default=str(datetime.datetime.now))
    class_name= Column(String(200), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

class course():
    def __init__(self):
        engine = create_engine('sqlite:///main.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_class(self, name):
        if self.session.query(Class).filter_by(name=name).first() is not None:
            return False
        self.session.add(Class(name=name))
        self.session.commit()
        return name
    
    def edit_class(self,name, new_name):
        class_to_edit = self.session.query(Class).filter_by(name=name).first()
        class_to_edit.name = new_name
        self.session.commit()

    def delete_class(self, name):
        class_to_delete = self.session.query(Class).filter_by(name=name).first()
        self.session.delete(class_to_delete)
        self.session.commit()
    
    def get_classes_list(self):
        classes = self.session.query(Class.name).all()
        classes = [i[0] for i in classes]
        return classes
    
    #folder stuff
    def add_folder(self, name, class_name):
        self.session.add(folder(name=name, class_name=class_name))
        self.session.commit()
    
    def edit_folder(self,name, new_name):
        folder_to_edit = self.session.query(folder).filter_by(name=name).first()
        folder_to_edit.name = new_name
        self.session.commit()
    
    def delete_folder(self, name):
        folder_to_delete = self.session.query(folder).filter_by(name=name).first()
        self.session.delete(folder_to_delete)
        self.session.commit()
    
    def get_folders_list(self, class_name):
        folders = self.session.query(folder.name).filter_by(class_name=class_name).all()
        folders = [i[0] for i in folders]
        return folders
    def get_all_courses(self):
        classes = self.session.query(Class.name).all()
        classes = [i[0] for i in classes]
        return classes
    def get_course_by_id(self, id):
        course = self.session.query(Class).filter_by(id=id).first()
        return course
    def get_class_and_ids(self):
        #returns tuple of the class name and its id
        classes = self.session.query(Class.name, Class.id).all()
        return list(classes)











if __name__ == '__main__':
    #example of how you can use it
    f=course()
    f2=Files()
    f.add_class('math')
    
    f.add_class('science')
    f.add_class('english')
    f.add_folder('week 1m', 'math')
    f.add_folder('week 2m', 'math')
    f.add_folder('week 3m', 'math')
    f.add_folder('week 1s', 'science')
    f.add_folder('week 2s', 'science')
    f.add_folder('week 3s', 'science')
  
    print(f.get_folders_list('math'))
    print(f.get_folders_list('science'))

    print(f.get_classes_list())
    f.delete_class('math')
    print(f.get_classes_list())
    print(f.get_folders_list('math'))
    #print(f2.add_file('math', 'week 1', 'notes', 100, '2020-01-01', 'pdf', 1,"l", 'C:\\Users\\user\\Desktop\\notes.pdf'))
    print(f2.add_file('file1', 'math', 'week 1', 'notes', 100, '2020-01-01', 'pdf', 1, 'C:\\Users\\user\\Desktop\\notes.pdf'))
    print(f2.get_files_list('math', 'week 1'))
