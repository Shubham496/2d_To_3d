import numpy as np
import cv2

def generate_3d_mesh(depth_map, grayscale_image, depth_threshold_percentage=10, height_scale=10.0, grayscale_height_scale=0.1):
    """ 
    Creats 3d mesh by multiplying grayscale image and depth map
    take agruments - depthmap, grayscale_image, depth_threshhold_percentage
    """
    height, width = depth_map.shape
    depth_threshold = np.percentile(depth_map, depth_threshold_percentage)
    
    result_image = cv2.adaptiveThreshold(grayscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 7)
    
    coords = []
    faces = []
    vertex_count = 0
    
    for y in range(height - 1):
        for x in range(width - 1):
            if depth_map[y, x] < depth_threshold:
                continue
            
            # Skip pixels that are black in the adaptive thresholded image
            if result_image[y, x] == 0:
                continue
            
            # Calculate height based on the depth map
            z1 = depth_map[y, x] * height_scale
            z2 = depth_map[y, x + 1] * height_scale
            z3 = depth_map[y + 1, x] * height_scale
            z4 = depth_map[y + 1, x + 1] * height_scale
            
            # Normalize brightness to the range [0, 1]
            brightness = grayscale_image[y, x] / 255.0
            
            # Calculate skip probability inversely proportional to brightness
            skip_probability = brightness* (1+ 0.005)
            
            # Skip the pixel based on the calculated skip probability
            if np.random.rand() < skip_probability:
                continue
            
            # Add extra height based on grayscale intensity
            z1 += brightness * grayscale_height_scale
            z2 += brightness * grayscale_height_scale
            z3 += brightness * grayscale_height_scale
            z4 += brightness * grayscale_height_scale
            
            coords.extend([(x, y, z1), (x + 1, y, z2), (x, y + 1, z3), (x + 1, y + 1, z4)])
            faces.extend([(vertex_count, vertex_count + 1, vertex_count + 3), (vertex_count, vertex_count + 3, vertex_count + 2)])
            vertex_count += 4
    
    return coords, faces

# Sample usage
# Assuming 'img' is the input image
# result_image = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
# coords, faces = generate_3d_mesh(depth_map, grayscale_image, result_image)


def save_mesh(filename, count=0, outputpath=''):
    # genrate mesh
    obj_path = filename.split('/')[-1].split('.')[0] + '_' + str(count) + '.obj'
    obj_path = outpath + '/' + obj_path
    with open(obj_path, 'w') as f:
        
        for coord in coords:
            f.write(f'v {coord[0]} {coord[1]} {coord[2]}\n')

        for face in faces:
            f.write(f'f {face[0]+1} {face[1]+1} {face[2]+1}\n')
    print('done... file path = ' + obj_path)
	
