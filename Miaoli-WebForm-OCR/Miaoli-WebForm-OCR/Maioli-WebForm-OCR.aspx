<%@ Page Async="true" Language="C#" AutoEventWireup="true" CodeBehind="Maioli-WebForm-OCR.aspx.cs" Inherits="Miaoli_WebForm_OCR.Maioli_WebForm_OCR" %>

<!DOCTYPE html>
<html>
<head runat="server">
    <title>YOLO + OCR Image Processing</title>
    <style type="text/css">
        #form1 {
            height: 236px;
        }
    </style>
</head>
<body>
    <form id="form1" runat="server" enctype="multipart/form-data">
        <asp:FileUpload ID="fileUploadImage" runat="server" />
        <asp:Button ID="Button1" runat="server" Text="處理影像" OnClick="Button1_Click" />
        <br /><br />
        <asp:Literal ID="Literal1" runat="server" Mode="PassThrough"></asp:Literal>

        <div>
            <asp:Literal ID="TestResults2" runat="server" Mode="PassThrough"></asp:Literal>
        </div>    
    </form>
</body>
</html>
