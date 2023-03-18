import AskLayout from "./AskLayout";
import {getFromStorage} from "@/helpers/localStorage";

const Ask = () => {
  var id = getFromStorage("user_id")

  const sendComment = (data) => {
    var formBody = [];

    let body = {
      user_id: id,
      title: data.title,
      content: data.content,
      string: data.tags,
    };

    for (let property in body) {
      var encodedKey = encodeURIComponent(property);
      var encodedValue = encodeURIComponent(body[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");

    let address = `http://127.0.0.1:8000/qna_app/question/add?${formBody}`;

    fetch(address, {
      method: "POST",
      mode: "no-cors",
      header: {
        Accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }).then((res) => {
      console.log(res.data);
    });
  };
  return (
    <>
      <AskLayout submitHandler={sendComment} />
    </>
  );
};

export default Ask;
