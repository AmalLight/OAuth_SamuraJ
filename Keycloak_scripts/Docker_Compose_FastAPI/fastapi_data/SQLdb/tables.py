from sqlalchemy     import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from SQLdb.database import Base

class Groups ( Base ) :

    __tablename__ = "groups"

    id =          Column ( Integer , primary_key = True  , index = True )
    group_name  = Column ( String  , unique      = True  , index = True )
    action_list = Column ( String  , unique      = False , index = True )

    groups = relationship ( "Actions" , back_populates = "actions" )


class Actions ( Base ) :

    __tablename__ = "actions"

    id =             Column ( Integer , primary_key = True  , index = True )
    action_name    = Column ( String  , unique      = True  , index = True )
    action_enable  = Column ( String  , unique      = False , index = True )
    action_disable = Column ( String  , unique      = False , index = True )
    action_cmd     = Column ( String  , unique      = False , index = True )

    actions = relationship ( "Groups" , back_populates = "groups" )
