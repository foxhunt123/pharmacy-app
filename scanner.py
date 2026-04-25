import cv2
from pyzbar import pyzbar

def scan_barcode():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            data = barcode.data.decode("utf-8")

            cap.release()
            cv2.destroyAllWindows()
            return data

        cv2.imshow("Scanner - натисни Q или ESC за изход", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == 27:  # ESC
            break

        # ако прозореца е затворен ръчно
        if cv2.getWindowProperty("Scanner - натисни Q или ESC за изход", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
    return None