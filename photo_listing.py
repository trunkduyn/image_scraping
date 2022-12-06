import csv
import json
import os


def recursive_image_finder(top_directory, image_list=None):
    if image_list is None:
        image_list = []

    try:
        dirs = os.listdir(path=top_directory)
    except PermissionError:
        print(f"permission error for {top_directory}")
        return image_list

    for d in dirs:
        cur_path = os.path.join(top_directory, d)
        if os.path.isdir(cur_path):
            recursive_image_finder(cur_path, image_list)
        elif os.path.isfile(cur_path):
            if d.lower().endswith(".png") or d.lower().endswith(".jpeg") or d.lower().endswith(".jpg"):
                image_list.append(cur_path)
            else:
                if d.lower().endswith('mp4'):
                    continue
                print(f"different file format found: {d}")
    return image_list


def write_label_studio_format_pinterest(directory, name, image_paths):
    prefix = "http://localhost:8001/"
    json_list = []
    for j, i_path in enumerate(image_paths):
        pinterest_board, file_name = i_path.split("/")[-2:]
        json_list.append({
            "data": {
                "image": prefix + f"{pinterest_board}/{file_name}",
                "ref_id": j,
                "pinterest_board": pinterest_board,
                "labels": [{"value": pinterest_board}],
            }
        })
    with open(os.path.join(directory, name), 'w') as outfile:
        json.dump(json_list, outfile, indent=4)


def write_label_studio_format(directory, name, image_paths):
    prefix = "http://localhost:8000/"
    json_list = [{
        "data": {
            "image": prefix + i_path.split("/")[-1],
            "ref_id": j,
        }
    } for j, i_path in enumerate(image_paths)]
    with open(os.path.join(directory, name), 'w') as outfile:
        json.dump(json_list, outfile, indent=4)


def write_image_paths(directory, name, image_paths):
    with open(os.path.join(directory, name), 'w') as outfile:
        writer = csv.writer(outfile)
        for i in image_paths:
            writer.writerow([i])
            print(i)

top_path = ""
image_paths = recursive_image_finder(top_path)
cur_dir = os.path.dirname(os.path.abspath(__file__))

write_label_studio_format(cur_dir, "label_studio_images.json", image_paths)

print(f"Recursively found {len(image_paths)} images")
print("run a server using `python3 -m http.server <PORT>` in the directory of the images")
