import Layout from "components/Layout/Layout";
import React, { useEffect, useState } from "react";
import { get } from "services/flowersService";
import { useSelector } from "react-redux";
import Images from "components/Images/Images";
import FormComment from "components/Forms/FormComment";
import DataShares from "components/DataShares/DataShares";
import Comment from "components/Comment/comment";
import HeadLine from "components/HeadLine/HeadLine";

const SharesCommunity = () => {
  const store = useSelector((state: any) => state);
  const [comments, setComments] = useState<string[]>([]);

  useEffect(() => {
    async function getData() {
      try {
        const data = (
          await get(
            store.isQuestion
              ? `community/questions/${store.question.question_id}/comments`
              : `community/observations/${store.question.observation_id}/comments`
          )
        ).data;
        setComments(
          data.sort(
            (a: any, b: any) =>
              new Date(b.create_dt).getTime() - new Date(a.create_dt).getTime()
          )
        );
      } catch (err) {
        console.log(err);
      }
    }
    getData();
  }, []);

  const showComments = comments.map((comment: any) => {
    return <Comment key={comment.comment_id} comment={comment} />;
  });

  return (
    <Layout>
      <div className="default-container">
        <div className="flex flex-col justify-center items-center max-w-[52.7%] m-auto">
          <HeadLine text={"שיתופים מהקהילה"} width={205} />
        </div>
        <DataShares />
        <div className="flex flex-col max-w-[100%] m-auto mt-5 gap-5">
          <Images
            username={store.question.username}
            photos={store.question.images}
            width={520}
            imageFromTheUser={true}
            isQuestion={store.isQuestion}
          />
          <FormComment setComments={setComments} />
          {showComments}
        </div>
      </div>
    </Layout>
  );
};

export default SharesCommunity;
