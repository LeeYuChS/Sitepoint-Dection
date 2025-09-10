import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO

"""
    create gui class about setting(button site or label...)
    last modify: 2025-08-27-16:56
"""

class YOLO_GUI:
    def __init__(self, win, yolo_weight):
        self.win = win
        self.yolo_weight = yolo_weight
        
        self.win.title("YOLO-Detection")
        self.win.geometry(f"780x650+0+0") # 視窗跳出來的位置，以字串作為輸入格式，前兩個數字為寬、高(width, height)，螢幕左上角為起始點(0, 0)，
        
        self.image_path = ""
        self.panel = None
        
        self.model = YOLO(self.yolo_weight)
        self.create_widgets()
        
    def create_widgets(self):
        top_frame = tk.Frame(self.win) # tk.Frame類似HTML的span或是div(一個容器包起來)
        
        """"
        tkinter的布局方式有3：
        1. pack()
            按先後順序布局在頁面上，可。
            padx、pady表示左右外、上下外邊距；ipadx、ipady表示左右內、上下內邊距。
            options:
                side --> 設定方位 side=tk.TOP / tk.BOTTOM / tk.LEFT / tk.RIGHT
                padx --> 設定左右外邊距 padx=??
                pady --> 設定上下外邊距 pady=??
                ipadx --> 設定左右內邊距 ipadx=?? (白話文的話就是說，文字置中之後左右兩邊跟button間的距離)
                ipady --> 設定上下內邊距 ipady=?? (白話文的話就是說，文字置中之後上下兩邊跟button間的距離)
        2. grid()
            將物件安排在一個「二維表格」內，指定row, column來決定擺放位置，格狀邏輯，對齊方便。
            options:
                row --> 物件放到哪一列 row=??
                column --> 物件放到哪一欄 column=??
                rowspan --> 物件放置位置要跨幾列 rowspan=??
                columnspan --> 物件放置位置要跨幾欄 columnspan=??
            e.g
            tk.Label(win, text="A").grid(row=17, column=0)
            tk.Label(win, text="B").grid(row=0, column=1)
            tk.Label(win, text="C").grid(row=1, column=4, columnspan=2)
        3. place()
            絕對 / 相對 座標定位
            options:
                x --> 物件左上角距離父容器左邊的像素距離 x=??
                y --> 物件左上角距離父容器上邊的像素距離 y=??
                relx --> 相對於父容器寬度的比例位置 (0.0~1.0) relx=??
                rely --> 相對於父容器高度的比例位置 (0.0~1.0) rely=??
                anchor --> 指定物件的哪個部分為定位參考點
                
                anchor='nw' 西北角（預設）--> 左上角
                anchor='n' 北方 --> 上方中央
                anchor='ne' 東北角 --> 右上角
                anchor='w' 西方 --> 左方中央
                anchor='center' 中心點 --> 正中央
                anchor='e' 東方 --> 右方中央
                anchor='sw' 西南角 --> 左下角
                anchor='s' 南方 --> 下方中央
                anchor='se' 東南角 --> 右下角
            e.g
            tk.Button(win, text="左上").place(x=10, y=10)
            tk.Button(win, text="中間").place(relx=0.5, rely=0.5, anchor='center')
            
        # *單一父元件下「不可混用pack, grid, place」，僅需選擇一種布局方式。
        """
        top_frame.pack(pady=10)
        # select button
        """
        command: button的驅動事件
        比較以下差異:
            1. command=self.select_image
                button建立的時候將'command指令'傳入，即將select_image傳入，而當事件驅動的時候才會執行select_image。
            2. command=self.select_image(args)
                button建立的時候將'command指令'傳入，但若這時候就將傳入參數寫進去，tk.Button會直接執行這個command，即執行select_image(args)。
        """
        btn_select = tk.Button(top_frame, text="Select Image", command=self.select_image, font=(12))
        btn_select.pack(side=tk.LEFT, pady=10)
        #detect button
        self.btn_detect = tk.Button(top_frame, text="Detect Image with YOLO", command=self.detect_image, font=(12), state="disabled")
        self.btn_detect.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(self.win, text="Select one first", font=(12))
        self.status_label.pack(pady=5)
        
    def select_image(self):
        """
        filedialog提供的四個常見函數：
            1. filedialog.askopenfilename(***options) --> 自動開啟選取窗口，手動選擇一個文件，返回文件路徑(字串)。
            2. filedialog.askopenfilenames(**options) --> 同時選擇多個文件，傳回一個tuple，包括所有選擇文件的路徑。
            3. filedialog.asksavesfile(**options) --> 選擇檔案儲存路徑並命名。
            4. filedialog.askdirectory(**options) --> 選擇一個資料夾，返回資料夾路徑。
        options 幾個常見可選參數：
            1. title -->指定檔案對話框的標題列文字 (對選擇檔案進行提示)。
            2. defaultextension --> 指定檔案的後綴檔案類型，例如: defaultextension=".jpg"，當使用者輸入一個檔案名稱為XXX時，檔案名稱會自動新增後綴為XXX.jpg，若輸入檔案本身具有後綴檔案類型，則忽略不管。
            3. filetypes --> 指定篩選檔案類型的下拉式選單選項，例如：filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
            4. initialdir --> 指定開啟儲存檔案的預設路徑(預設路徑是目前資料夾)
            5. multiple --> 是否開啟多個文件
        """
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if len(path)>0:
            self.image_path = path
            
            original_image = cv2.imread(self.image_path)
            resized_image = self.resize_image(original_image)
            
            self.display_image(resized_image)
            """
            button state: 
                1. button.config(state="normal") --> 正常狀態
                2. button.config(state="disable") --> 不能按，跟C#差不多
                3. button.config(state="activate") --> 滑鼠放上去的時候介面會切換(視覺效果)，但我感覺不出來：）
            """
            self.btn_detect.config(state="normal") # --> 一開始先disable，使用者上傳影像(發現path長度大於0，表示有人選照片了)，再將狀態打開。
            self.status_label.config(text=f"Loaded: {self.image_path.split('/')[-1]}")
                
    def detect_image(self):
        self.status_label.config(text="Detecting...")
        """
            update_idletasks():
                1. 需要立即更新GUI顯示但不想阻塞主程式，調用時所有子控件都會被更新
                2. 空閒任務才被更新，Tkinter判定「系統目前沒有其他更高優先序事件」才會執行的背景更新任務(使用者可以立即看到UI變化)
            update():
                1. 在Tkinter的事件迴圈中，所有與視窗互動相關的任務都會被排進一個事件佇列，而「待處理事件」指的是在這個佇列裡尚未被主迴圈處理的項目，通常包含：
                    使用者輸入事件 --> 滑鼠點擊、鍵盤按鍵、視窗調整
                    重繪事件 --> 物件需重新繪製(外觀變化、尺寸改變)
                    排程事件 --> 透過 widget.after(ms, func) 設定的延遲呼叫，時間一到就會被放進佇列等待執行
                2. 容易造成視窗卡住，重入主迴圈
        """
        self.win.update_idletasks()
        
        results = self.model(self.image_path)
        annotated_image = results[0].plot()
        
        resized_annotated_image = self.resize_image(annotated_image)
        self.display_image(resized_annotated_image)
        self.status_label.config(text="Detected!")
        
    def display_image(self, image_np):
        """
        cv2 vs. Image
        1.  cv2.imread() --> BGR (cv2.imwrite()相當於BGR to RGB儲存)
            Image.open() --> RGB
        2.  cv2 shape --> (Height, Width, Channel) (C, H, W)的順序通常用於Pytorch or Tensorflow
            Image shape --> (Width, Height)
                要看Image的channel可以，
                from PIL import Image
                img = Image.open("photo.jpg")
                channels = len(img.getbands())
        3.  cv2以numpy數組形式載入記憶體
            Image以Image物件載入記憶體
        """
        
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB) # BGR轉RGB
        image_pil = Image.fromarray(image_rgb) # RGB array轉Pillow Image物件
        image_tk = ImageTk.PhotoImage(image_pil) # Pillow Image轉成Tkinter PhotoImage
        
        """
            panel作為image的容器放置在win上，值得注意的是：
            Tkinter是Python對Tcl/Tk GUI工具包的一個「介面」或「包裝」(API)，當使用者建立一個tk.Label並設定image屬性時，背後會做兩件事，
                1. Python建立了一個ImageTk.PhotoImage物件
                2. Tkinter將這個Python物件的影像資料傳給底層的Tcl/Tk引擎，由Tcl/Tk負責在win上繪製影像
            問題在於，Tcl/Tk引擎只在乎傳入的影像資料，他不在乎對於Python PhotoImage物件的強參考，
            「在display_image這個method中」，結束之後image_tk就被當作弱參考以垃圾回收機制(garbage collection)被處理掉導致影像不會顯示，
            但「在YOLO_GUI這個class中」，他是一個主類別，而self.panel則是主類別實例的一個屬性，所以即使display_image這個method已經結束了，也不會釋放image_tk，GUI才會正常顯示圖像。
        """
        if self.panel is None:
            self.panel = tk.Label(self.win, image=image_tk)
            self.panel.image = image_tk
            self.panel.pack(padx=10, pady=10)
        else:
            self.panel.configure(image=image_tk) # config，程式執行時間查詢或修改Widget的屬性(這裡的用法相當於動態更新這個label的設定)
            self.panel.image = image_tk
    
    def resize_image(self, image, max_width=780, max_height=500):
        """
            以cv2讀圖，所以是(Height, Width, Channel)，而我要(h, w) 所以 image.shape[:2]。
            取max_height跟max_width的縮放最小值，目的為保持長寬比不變，且若圖高度、寬度比上限高，就縮小，
            若ratio < 1，表示至少有一邊大於指定上限，必須縮小；若ratio > 1，表示圖在限制內，不須多做處理。
        """
        h, w = image.shape[:2]
        ratio = min(max_height/h, max_width/w)
        
        if ratio<1:
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return image




