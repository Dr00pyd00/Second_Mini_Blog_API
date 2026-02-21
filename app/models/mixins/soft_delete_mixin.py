from time import timezone

from sqlalchemy import Column, Datetime, func



class SoftDeleteMixin():

    # if delete_at is None :  not soft deleted 
    # else : object is deleted!

    deleted_at = Column(
        Datetime(timezone=True),
        nullable=False
        )

    def soft_delete(self):
        self.deleted_at = func.now()
    
    def restore_from_soft_delete(self):
        self.deleted_at = None