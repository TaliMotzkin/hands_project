import cv2

# Create a black image
test_image = cv2.imread('./trial.jpeg')  # ensure the path and image file are correct

# Display the image
cv2.imshow('Test Image', test_image)

# Wait for a key press indefinitely
cv2.waitKey(0)
# Close the window
cv2.destroyAllWindows()