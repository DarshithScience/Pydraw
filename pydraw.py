import streamlit as st
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

def dodgeV2(x, y):
        return cv2.divide(x, 255 - y, scale=256)

def convertto_watercolorsketch(inp_img):
	img_1 = cv2.edgePreservingFilter(inp_img, flags=2, sigma_s=50, sigma_r=0.8)
	img_water_color = cv2.stylization(img_1, sigma_s=100, sigma_r=0.5)
	return(img_water_color)

def pencilsketch(inp_img):
        img_gray = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
        img_invert = cv2.bitwise_not(img_gray)
        img_smoothing = cv2.GaussianBlur(img_invert, (21, 21),sigmaX=0, sigmaY=0)
        final_img = dodgeV2(img_gray, img_smoothing)
        return(final_img)

def load_an_image(image):
	img = Image.open(image)
	return img

def main():
	
	st.title('WEB APPLICATION TO CONVERT IMAGE TO SKETCH')
	st.write("This is an application developed for converting\
	your ***image*** to a ***Water Color Sketch*** OR ***Pencil Sketch***")
	st.subheader("Please Upload your image")
	
	image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])

	if image_file is not None:
		
		option = st.selectbox('How would you like to convert the image',
							('Convert to water color sketch',
							'Convert to pencil sketch'))
		if option == 'Convert to water color sketch':
			image = Image.open(image_file)
			final_sketch = convertto_watercolorsketch(np.array(image))
			im_pil = Image.fromarray(final_sketch)
			col1, col2 = st.columns(2)
			with col1:
				st.header("Original Image")
				st.image(load_an_image(image_file), width=250)

			with col2:
				st.header("Water Color Sketch")
				st.image(im_pil, width=250)
				buf = BytesIO()
				img = im_pil
				img.save(buf, format="JPEG")
				byte_im = buf.getvalue()
				st.download_button(
					label="Download image",
					data=byte_im,
					file_name="watercolorsketch.png",
					mime="image/png"
				)

		if option == 'Convert to pencil sketch':
			image = Image.open(image_file)
			final_sketch = pencilsketch(np.array(image))
			im_pil = Image.fromarray(final_sketch)
			col1, col2 = st.columns(2)
			with col1:
				st.header("Original Image")
				st.image(load_an_image(image_file), width=250)

			with col2:
				st.header("Pencil Sketch")
				st.image(im_pil, width=250)
				buf = BytesIO()
				img = im_pil
				img.save(buf, format="JPEG")
				byte_im = buf.getvalue()
				st.download_button(
					label="Download image",
					data=byte_im,
					file_name="pencilsketch.png",
					mime="image/png"
				)


if __name__ == '__main__':
	main()
