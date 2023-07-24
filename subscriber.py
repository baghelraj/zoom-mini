# Open CV to display incoming frame
import cv2
# Redis to subscribe
import redis
# Numpy to convert message packet to 2D array of pixels.
import numpy as np
 
client = redis.Redis(host='127.0.0.1', port=6379)
# Creating a Pub Sub client to subscribe to some channels.
client_channel = client.pubsub()


# Let's subscribe to other user's channel.
client_channel.subscribe("user_1")


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 360))
count = 0 
try:
    # Listening to messages in the channel
    for item in client_channel.listen():    
        if item["type"] != "message":
            continue


        # For every message received in the channel, converting the bytes to a 2D array.
        frame = np.frombuffer(item["data"], dtype="uint8").reshape(360, 640, 3)
    
        print("frame", frame)

        if count < 100:
            out.write(frame)
            count = count + 1
        else:
            out.release()    
        
        # Displaying this frame back to the User client.
        cv2.imshow("VideoFrame", frame)
    
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    client_channel.unsubscribe()
    cv2.destroyAllWindows()
    out.release()