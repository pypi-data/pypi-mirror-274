
import os, sys
# ====== experimentation block ======== #
current_path  = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)
# ====== experimentation block ======== #



from kitchenware_model_package import __version__ as _version
from kitchenware_model_package.config import core
from kitchenware_model_package import predict



def test_prediction(img_file):
    # given
    filename = img_file
    expected_class =  'fork'

    # when
    pred =  predict.make_single_img_prediction(image_name = filename, 
                                           image_dir = core.IMAGES)
    
    # Then
    assert pred['image_class'] is not None
    assert pred['version'] == _version
    assert pred['image_class'] == expected_class
