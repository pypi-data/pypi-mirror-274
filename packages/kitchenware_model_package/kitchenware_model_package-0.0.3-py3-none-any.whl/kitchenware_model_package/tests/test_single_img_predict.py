# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from kitchenware_model_package import __version__ as _version
from kitchenware_model_package.config import core
from kitchenware_model_package.predict import make_single_img_prediction



def test_prediction(img_file):
    # given
    filename = img_file
    expected_class =  'fork'

    # when
    pred =  make_single_img_prediction(file = filename, 
                                           folder = core.IMAGES)
    
    # Then
    assert pred['image_class'] is not None
    assert pred['version'] == _version
    assert pred['image_class'][0] == expected_class
