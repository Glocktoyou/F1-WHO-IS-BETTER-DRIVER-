class MockF1Session:
    def get_circuit_info(self):
        import numpy as np
        # Return a simple square as track outline
        return {'Layout': np.array([[0,0],[0,1],[1,1],[1,0],[0,0]])}
