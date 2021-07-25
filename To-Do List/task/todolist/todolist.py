from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime , timedelta

Base = declarative_base()


class TaskCard(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date)

    def __repr__(self):
        return self.string_field


class TaskService:
    def __init__(self, session_):
        self.session_ = session_

    def add_card(self, task_, date_):
        new_data = TaskCard(task=task_,
                            deadline=date_)
        self.session_.add(new_data)
        self.session_.commit()
        print("The task has been added!")

    def get_card_by_name(self, task_):
        return self.session_.query(TaskCard).filter(TaskCard.task == task_).all()

    def get_cards_by_date(self, date_):
        return self.session_.query(TaskCard).filter(TaskCard.deadline == date_).all()

    def get_range_tasks(self, start_, end_):
        return self.session_.query(TaskCard).filter(TaskCard.deadline.between(start_, end_)).order_by(TaskCard.deadline).all()

    def get_cards(self):
        return self.session_.query(TaskCard).order_by(TaskCard.deadline).all()

    def delete_card(self,  task_):
        self.session_.delete(task_)
        self.session_.commit()
        print("The task has been deleted!")

    def get_before_date(self, date_):
        return self.session_.query(TaskCard).filter(TaskCard.deadline < date_).all()

    def today_tasks(self):
        tasks_ = self.get_cards_by_date(datetime.today().date())
        print(datetime.today().strftime("Today: %d %b:"))
        if len(tasks_) == 0:
            print("Nothing to do!")
        else:
            for n_ in range(len(tasks_)):
                print("{}. {}".format(n_ + 1, tasks_[n_].task))

    def add_task(self):
        print("Enter task")
        task_name_ = input()
        print("Enter deadline")
        deadline_ = datetime.strptime(input(), "%Y-%m-%d")
        print("dead", deadline_)
        self.add_card(task_name_, deadline_)

    def delete_task(self):
        tasks_ = self.get_cards()
        if len(tasks_) == 0:
            print("Nothing to delete")
        else:
            print("Choose the number of the task you want to delete:")
            for n_ in range(len(tasks_)):
                print("{}. {}. {}".format(n_ + 1, tasks_[n_].task, tasks_[n_].deadline.strftime("%d %b:")))
            task_number = input()
            try:
                if int(task_number) in (1, len(tasks_) + 1):
                    self.delete_card(tasks_[int(task_number) - 1])
            except ValueError:
                print("Type error")

    def week_tasks(self):
        date_ = datetime.today()
        for n_ in range(0, 7):
            d_ = date_ + timedelta(days=n_)
            print(d_.strftime("%A %d %b:"))
            tasks_ = self.get_cards_by_date(d_.date())
            if len(tasks_) == 0:
                print("Nothing to do!")
                print()
            else:
                for x_ in range(len(tasks_)):
                    print("{}. {}".format(x_ + 1, tasks_[x_].task))
                    print()

    def all_tasks(self):
        tasks_ = self.get_cards()
        if len(tasks_) == 0:
            print("Nothing to do!")
        else:
            print("All tasks:")
            for n_ in range(len(tasks_)):
                print("{}. {}. {}".format(n_ + 1, tasks_[n_].task, tasks_[n_].deadline.strftime("%d %b:")))

    def missed_task(self):
        print("Missed tasks:")
        tasks_ = service.get_before_date(datetime.today().date())
        if len(tasks_) == 0:
            print("Nothing is missed!")
        else:
            for n_ in range(len(tasks_)):
                print("{}. {}. {}".format(n_ + 1, tasks_[n_].task, tasks_[n_].deadline.strftime("%d %b:")))
        print()


def main_menu():
    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")
        choice_ = input()
        if choice_ == "1":
            service.today_tasks()
        elif choice_ == "2":
            service.week_tasks()
        elif choice_ == "3":
            service.all_tasks()
        elif choice_ == "4":
            service.missed_task()
        elif choice_ == "5":
            service.add_task()
        elif choice_ == "6":
            service.delete_task()
        elif choice_ == "0":
            print("Bye!")
            break
        else:
            print("{} is not an option".format(choice_))


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
service = TaskService(session)
main_menu()

