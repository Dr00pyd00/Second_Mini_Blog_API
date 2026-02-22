from sqlalchemy import Column, DateTime, func


class SoftDeleteMixin():

    # if delete_at is None :  not soft deleted 
    # else : object is deleted!
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True
        )

    def soft_delete(self):
        self.deleted_at = func.now()
    
    def restore_from_soft_delete(self):
        self.deleted_at = None