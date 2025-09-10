using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Web.Hosting;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Miaoli_WebForm_OCR
{
    public partial class Maioli_WebForm_OCR : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {

        }
        // 考慮web.config 虛擬路徑轉實體路徑
        private static string ResolvePath(string pathSetting)
        {
            if (string.IsNullOrWhiteSpace(pathSetting))
                throw new InvalidOperationException("StorageRoot not configured");

            if (pathSetting.StartsWith("~"))
                return HostingEnvironment.MapPath(pathSetting);

            return pathSetting;
        }
        private static string EnsureDir(string physicalPath)
        {
            Directory.CreateDirectory(physicalPath); // mkdir
            return physicalPath;
        }
        protected async void Button1_Click(object sender, EventArgs e)
        {
            if (!fileUploadImage.HasFile)
            {
                Literal1.Text = "Please upload an image first.";
                return;
            }
            try
            {
                // 產生時戳資料夾
                var storageRootCfg = ConfigurationManager.AppSettings["StorageRoot"];
                var storageRoot = ResolvePath(storageRootCfg);
                var datetimeFolder = DateTime.Now.ToString("yyyyMMdd_HHmmssfff"); // e.g 20250820_164401123
                var uploadDir = EnsureDir(Path.Combine(storageRoot, "Uploads", datetimeFolder));

                // 保存上傳檔案到該資料夾（使用 GUID 檔名）
                var ext = Path.GetExtension(fileUploadImage.FileName);
                if (string.IsNullOrWhiteSpace(ext))
                {
                    ext = ".bin";
                }

                var safeName = $"{Guid.NewGuid()}{ext}";
                var savedPath = Path.Combine(uploadDir, safeName);
                fileUploadImage.SaveAs(savedPath);

                /* 只傳 datetime_folder 給python api 
                   python端在join路徑 
                */
                var apiResultBatch = await CallFastApiWithDatetimeFolderAsync(datetimeFolder);
                //Literal1.Text = "<pre>" + HttpUtility.HtmlEncode(apiResultBatch) + "</pre>";

                JObject joBatch = JObject.Parse(apiResultBatch);
                JArray results = (JArray)joBatch["results"];

                StringBuilder sb = new StringBuilder();
                sb.Append("<table border='1' style='border-collapse:collapse; width:100%;'>");
                sb.Append("<tr><th>YOLO Class</th><th>OCR</th><th>Bounding Box</th><th>Cropped Images</th></tr>");

                foreach (var item in results)
                {
                    string yoloCls;
                    if (item["yolo_cls"] != null)
                    {
                        yoloCls = item["yolo_cls"].ToString();
                    }
                    else
                    {
                        yoloCls = null;
                    }

                    string ocrText;
                    if (item["ocr_text"] != null)
                    {
                        ocrText = item["ocr_text"].ToString();
                    }
                    else
                    {
                        ocrText = null;
                    }

                    string bbox;
                    if (item["bounding_box"] != null)
                    {
                        bbox = string.Join(", ", item["bounding_box"].ToObject<int[]>());
                    }
                    else
                    {
                        bbox = null;
                    }

                    string croppedImg;
                    if (item["cropped_image"] != null)
                    {
                        croppedImg = item["cropped_image"].ToString();
                    }
                    else
                    {
                        croppedImg = null;
                    }


                    sb.Append("<tr>");
                    sb.AppendFormat("<td>{0}</td>", yoloCls);
                    sb.AppendFormat("<td>{0}</td>", HttpUtility.HtmlEncode(ocrText));
                    sb.AppendFormat("<td>{0}</td>", bbox);
                    sb.AppendFormat("<td><img src='{0}' width='150'/></td>", croppedImg);
                    sb.Append("</tr>");
                }
                sb.Append("</table>");

                TestResults2.Text = sb.ToString();

            }
            catch (Exception ex)
            {
                Literal1.Text = "Error: " + HttpUtility.HtmlEncode(ex.Message);
            }
        }
        private async Task<string> CallFastApiWithDatetimeFolderAsync(string datetimeFolder)
        {
            using (var client = new HttpClient())
            using (var form = new MultipartFormDataContent())
            {
                // form就是要傳給api的內容
                form.Add(new StringContent(datetimeFolder), "datetime_folder");

                var apiUrl = "http://localhost:8000/inference_batch";
                var resp = await client.PostAsync(apiUrl, form);
                resp.EnsureSuccessStatusCode();
                return await resp.Content.ReadAsStringAsync();
            }
        }
    }
}

//using System;
//using System.Configuration;
//using System.IO;
//using System.Linq;                       // 用於 .Select
//using System.Net.Http;
//using System.Net.Http.Headers;
//using System.Text;
//using System.Threading.Tasks;
//using System.Web;
//using System.Web.Hosting;
//using System.Web.UI;
//using Newtonsoft.Json.Linq;


//namespace Miaoli_WebForm_OCR
//{
//    public partial class WebForm1 : System.Web.UI.Page
//    {
//        protected void Page_Load(object sender, EventArgs e)
//        {

//        }
//        // 考慮web.config 虛擬路徑轉實體路徑
//        private static string ResolvePath(string pathSetting)
//        {
//            if (string.IsNullOrWhiteSpace(pathSetting))
//                throw new InvalidOperationException("StorageRoot not configured");

//            if (pathSetting.StartsWith("~"))
//                return HostingEnvironment.MapPath(pathSetting);

//            return pathSetting;
//        }
//        private static string EnsureDir(string physicalPath)
//        {
//            Directory.CreateDirectory(physicalPath); // mkdir
//            return physicalPath;
//        }
//        protected async void Button1_Click(object sender, EventArgs e)
//        {
//            if (!fileUploadImage.HasFile)
//            {
//                Literal1.Text = "Please upload an image first.";
//                return;
//            }
//            try
//            {
//                // 產生時戳資料夾
//                var storageRootCfg = ConfigurationManager.AppSettings["StorageRoot"];
//                var storageRoot = ResolvePath(storageRootCfg);
//                var datetimeFolder = DateTime.Now.ToString("yyyyMMdd_HHmmssfff"); // e.g 20250820_164401123
//                var uploadDir = EnsureDir(Path.Combine(storageRoot, "Uploads", datetimeFolder));

//                // 保存上傳檔案到該資料夾（使用 GUID 檔名）
//                var ext = Path.GetExtension(fileUploadImage.FileName);
//                if (string.IsNullOrWhiteSpace(ext))
//                {
//                    ext = ".bin";
//                }

//                var safeName = $"{Guid.NewGuid()}{ext}";
//                var savedPath = Path.Combine(uploadDir, safeName);
//                fileUploadImage.SaveAs(savedPath);

//                /* 只傳 datetime_folder 給python api 
//                   python端在join路徑 
//                */
//                var apiResultBatch = await CallFastApiWithDatetimeFolderAsync(datetimeFolder);
//                //Literal1.Text = "<pre>" + HttpUtility.HtmlEncode(apiResultBatch) + "</pre>";

//                JObject joBatch = JObject.Parse(apiResultBatch);
//                JArray results = (JArray)joBatch["results"];

//                StringBuilder sb = new StringBuilder();
//                sb.Append("<table border='1' style='border-collapse:collapse; width:100%;'>");
//                sb.Append("<tr><th>YOLO Class</th><th>OCR</th><th>Bounding Box</th><th>Cropped Images</th></tr>");

//                foreach (var item in results)
//                {
//                    string yoloCls;
//                    if (item["yolo_cls"] != null)
//                    {
//                        yoloCls = item["yolo_cls"].ToString();
//                    }
//                    else
//                    {
//                        yoloCls = null;
//                    }

//                    string ocrText;
//                    if (item["ocr_text"] != null)
//                    {
//                        ocrText = item["ocr_text"].ToString();
//                    }
//                    else
//                    {
//                        ocrText = null;
//                    }

//                    string bbox;
//                    if (item["bounding_box"] != null)
//                    {
//                        bbox = string.Join(", ", item["bounding_box"].ToObject<int[]>());
//                    }
//                    else
//                    {
//                        bbox = null;
//                    }

//                    string croppedImg;
//                    if (item["cropped_image"] != null)
//                    {
//                        croppedImg = item["cropped_image"].ToString();
//                    }
//                    else
//                    {
//                        croppedImg = null;
//                    }


//                    sb.Append("<tr>");
//                    sb.AppendFormat("<td>{0}</td>", yoloCls);
//                    sb.AppendFormat("<td>{0}</td>", HttpUtility.HtmlEncode(ocrText));
//                    sb.AppendFormat("<td>{0}</td>", bbox);
//                    sb.AppendFormat("<td><img src='{0}' width='150'/></td>", croppedImg);
//                    sb.Append("</tr>");
//                }
//                sb.Append("</table>");

//                TestResults2.Text = sb.ToString();

//            }
//            catch (Exception ex)
//            {
//                Literal1.Text = "Error: " + HttpUtility.HtmlEncode(ex.Message);
//            }
//        }
//        private async Task<string> CallFastApiWithDatetimeFolderAsync(string datetimeFolder)
//        {
//            using (var client = new HttpClient())
//            using (var form = new MultipartFormDataContent())
//            {
//                // form就是要傳給api的內容
//                form.Add(new StringContent(datetimeFolder), "datetime_folder");

//                var apiUrl = "http://localhost:8000/inference_batch";
//                var resp = await client.PostAsync(apiUrl, form);
//                resp.EnsureSuccessStatusCode();
//                return await resp.Content.ReadAsStringAsync();
//            }
//        }
//    }
//}