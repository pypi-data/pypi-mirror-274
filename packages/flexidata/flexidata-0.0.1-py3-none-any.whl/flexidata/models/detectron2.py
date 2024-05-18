from flexidata.utils.constants import ElementType
import layoutparser as lp
import logging
import torchvision
import torch


CONFIG_PATH = "lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config"
MODEL_PATH = "/app/flexi-data/src/models/PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/model_final.pth"
LABEL_MAP = {
    0: ElementType.TEXT,
    1: ElementType.TITLE,
    2: ElementType.LIST,
    3: ElementType.TABLE,
    4: ElementType.FIGURE,
}

EXTRA_CONFIG=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5]


class DetectronModel:

    def predict(self, page_image):
        layouts = self.model.detect(page_image)
        # text_blocks = lp.Layout([b for b in layouts if b.type=='Text'])
        # self.post_process(text_blocks)
        # layouts = [layout for layout in layouts if layout.type != 'None']
        return layouts
    
    def get_text_block(self, block):
        x1, y1, x2, y2 = block.coordinates
        text = block.text
        type = block.type
        prob = block.score
        print(text, type)

    def initialize(self, config_path=None, model_path=None, label_map=None, extra_config=None):
        if not lp.is_detectron2_available():
            raise ImportError(
                "Failed to load the Detectron2 model. Ensure that the Detectron2 "
                "module is correctly installed.",
            )
        config_path = CONFIG_PATH if config_path is None else config_path
        label_map = LABEL_MAP if label_map is None else label_map
        extra_config = EXTRA_CONFIG if extra_config is None else extra_config
        model_path = MODEL_PATH if model_path is None else model_path
        logging.info(f"start downloading model for detectron2 {config_path} model_path = {model_path}")
        self.model = lp.Detectron2LayoutModel(
            str(config_path),
            model_path= model_path,
            label_map=label_map,
            extra_config=extra_config   
        )

    def post_process(self, layouts):
        for bbox_1 in layouts:
            for bbox_2 in layouts:
                if bbox_1 != bbox_2:
                    self.refine(bbox_1, bbox_2)
            

    def refine(self, block_1, block_2):
        bbox_1 = self.draw_bbox(block_1)
        bbox_2 = self.draw_bbox(block_2)

        iou = self.compute_iou(bbox_1, bbox_1)

        if iou.tolist()[0][0] != 0:

            a1 = self.compute_area(bbox_1)
            a2 = self.compute_area(bbox_2)

            block_2.set(type='None', inplace= True) if a1 > a2 else block_1.set(type='None', inplace= True)

    def draw_bbox(self, box):
        x1 = box.block.x_1
        y1 = box.block.y_1
        x2 = box.block.x_2
        y2 = box.block.y_2

        return torch.tensor([[x1, y1, x2, y2]], dtype=torch.float)
    
    def compute_iou(self, bbox_1, bbox_2):
        return torchvision.ops.box_iou(bbox_1, bbox_2)
    
    def compute_area(self, box):
        width = box.tolist()[0][2] - box.tolist()[0][0]
        length = box.tolist()[0][3] - box.tolist()[0][1]
        area = width*length
        return area
