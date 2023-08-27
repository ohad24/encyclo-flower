import Layout from "components/Layout/Layout";
import React, { useEffect, useState } from "react";
import { get } from "services/flowersService";
import Suggestions from "components/Suggestions/Suggestions";
import InfiniteScroll from "react-infinite-scroll-component";
import HeadLine from "components/HeadLine/HeadLine";

const Shares = () => {
  const [observations, setObservations] = useState<any[]>([]);
  const [page, setPage] = useState<number>(9);
  const [hasMore, setHasMore] = useState<boolean>(true);

  useEffect(() => {
    async function getData() {
      try {
        const observations = (
          await get("community/observations/?answer_filter=all&skip=0&limit=9")
        ).data;
        setObservations(observations);
      } catch (err) {
        console.log(err);
      }
    }
    getData();
  }, []);

  const fetchData = async () => {
    try {
      const data = (
        await get(
          `community/observations/?answer_filter=all&skip=${page}&limit=9`
        )
      ).data;
      if (data.length === 0) {
        setHasMore(false);
      } else {
        setObservations([...observations, ...data]);
        setPage(page + 9);
      }
    } catch (err) {
      console.log(err);
    }
  };

  const showObservations = observations.map((observation) => (
    <Suggestions
      key={observation.observation_id}
      str={"observation_text"}
      question={observation}
      isQuestion={false}
    />
  ));

  return (
    <Layout>
      <div className="default-container">
        <div className="flex flex-col justify-center items-center max-w-[52.7%] m-auto">
          <HeadLine text={"שיתופים מהקהילה"} width={203} />
        </div>
        <InfiniteScroll
          className="flex flex-col items-center gap-4"
          dataLength={observations.length} //This is important field to render the next data
          next={() => fetchData()}
          hasMore={hasMore}
          loader={<h2>טוען...</h2>}
        >
          {showObservations}
        </InfiniteScroll>
      </div>
    </Layout>
  );
};

export default Shares;
