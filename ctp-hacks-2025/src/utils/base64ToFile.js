//Converts a base64 string to a file object. It takes the frontend's base64 image string, decodes it, builds the raw bytes, and wraps them into a file object so you can send it to the backend 
export function base64ToFile(base64, filename = "upload.png", contentType = "image/png") {
  //If base64 is a full URL then split it on the comma and only take the raw base64 part
    const clean = base64.includes(",") ? base64.split(",")[1] : base64;
  //decode the base64 string into a normal inary string   
  const byteChars = atob(clean);
  //create an array of character codes
  const byteNums = new Array(byteChars.length);
  for (let i = 0; i < byteChars.length; i++) 
    {
        byteNums[i] = byteChars.charCodeAt(i);
    }
   //convert the array of
   //  codes into a array of bytes  
  const byteArray = new Uint8Array(byteNums);
  //wrap byte array into a file object with the name and type 
  return new File([byteArray], filename, { type: contentType });
}