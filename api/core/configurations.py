import os


class Config:
    
    @property
    def env(self):
        return os.environ.get('ENV', 'lcl')
    
