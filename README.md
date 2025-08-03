

# image-noise-expander

![](.docs/screenshot.png)

## Installation
```bash
uv sync
```

## Usage
```bash
uv run app.py
```

## Results

| Input |
|:---------------:|
| ![](.docs/input_cat.jpg) |

### Outside Mode

| TOP | BOTTOM | LEFT | RIGHT |
|:---------------:|:---------------:|:---------------:|:----------------:|
|![](.docs/output_out_top.png) | ![](.docs/output_out_bottom.png) | ![](.docs/output_out_left.png) | ![](.docs/output_out_right.png) |
|![](.docs/output_out_top_mask.png) | ![](.docs/output_out_bottom_mask.png) | ![](.docs/output_out_left_mask.png) | ![](.docs/output_out_right_mask.png) |

### Inside Mode

| TOP | BOTTOM | LEFT | RIGHT |
|:---------------:|:---------------:|:---------------:|:----------------:|
|![](.docs/output_in_top.png) | ![](.docs/output_in_bottom.png) | ![](.docs/output_in_left.png) | ![](.docs/output_in_right.png) |
|![](.docs/output_in_top_mask.png) | ![](.docs/output_in_bottom_mask.png) | ![](.docs/output_in_left_mask.png) | ![](.docs/output_in_right_mask.png) |
