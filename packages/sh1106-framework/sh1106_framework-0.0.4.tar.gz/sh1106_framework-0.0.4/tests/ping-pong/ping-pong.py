from src.sh1106_framework.framework.states.state_manager import StateManager
from src.sh1106_framework.sh1106_framework import SH1106Framework
from ping import PingPage

def __init():
    SH1106Framework.register_font("default", "assets/default_font.json")
    SH1106Framework.register_images("assets/icons.json")
    
    SH1106Framework.register_routes(
        default_route="splash",
        routes={
            "splash": PingPage(StateManager)
        }
    )
    
    SH1106Framework.begin(port=1, address=0x3C)
    pass
    
if __name__ == "__main__":
    __init()