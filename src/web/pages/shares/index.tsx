import Layout from "components/Layout/Layout";
import React, { useEffect, useState } from "react";
import { getAll } from "services/flowersService";
import Suggestions from "components/Suggestions/Suggestions";
import InfiniteScroll from "react-infinite-scroll-component";

const Shares = () => {
  const [observations, setObservations] = useState<any[]>([]);
  const [page, setPage] = useState<number>(9);
  const [hasMore, setHasMore] = useState<boolean>(true);

  useEffect(() => {
    async function getData() {
      try {
        const observations = (
          await getAll(
            "community/observations/?answer_filter=all&skip=0&limit=9"
          )
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
        await getAll(
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

  return (
    <Layout>
      <div className="default-container">
        <div className="flex flex-col justify-center items-center max-w-[52.7%] m-auto">
          <div className="flex items-center justify-center my-5 ">
            <p className="font-bold text-secondary  border-b-4  border-b-primary mb-7 text-2xl max-w-[203px] text-center ">
              שיתופים מהקהילה
            </p>
          </div>
        </div>
        <InfiniteScroll
          className="flex flex-col items-center gap-4"
          dataLength={observations.length} //This is important field to render the next data
          next={() => fetchData()}
          hasMore={hasMore}
          loader={<h2>טוען...</h2>}
        >
          {observations.map((observation) => (
            <Suggestions
              str={"observation_text"}
              question={observation}
              isQuestion={false}
            />
          ))}
        </InfiniteScroll>
      </div>
    </Layout>
  );
};

export default Shares;
