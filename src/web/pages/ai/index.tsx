import React from "react";
import Layout from "../../components/Layout/Layout";
import { useSelector } from "react-redux";
import MenuAI from "components/MenuAI/MenuAI";
import ModalDirective from "components/Modals/ModalDirective";
import ImagePlant from "components/ImagePlant/ImagePlant";
import SearchResults from "components/SearchResults/SearchResults";
import SearchResult from "components/SearchResult/SearchResult";
import { useRouter } from "next/router";
import { nanoid } from "nanoid";

const FlowerAI = () => {
  const [isOpen, setIsOpen] = React.useState(false);
  const router = useRouter();
  const store = useSelector((state: any) => state);

  return (
    <Layout>
      <div className="default-container">
        <MenuAI setIsOpen={setIsOpen} />
        <br />
        <ModalDirective isOpen={isOpen} setIsOpen={setIsOpen} />
        <div
          className="flex flex-row flex-wrap max-w-[768px] m-auto gap-5 items-center" // items-center
        >
          {" "}
          {router.query.im ? (
            <img
              alt="undefined"
              src={router.query.im as string}
              className="w-[350px] h-[285px] rounded-3xl m-auto md:m-0 object-cover"
            />
          ) : (
            Array.from(store.selectedImages).map((selectedImage, index) => {
              return <ImagePlant key={nanoid()} index={index} />;
            })
          )}
        </div>
        <SearchResults length={store.results.length} />

        {store.results &&
          store.results.map((result: any, index: number) => {
            return <SearchResult result={result} index={index} />;
          })}
      </div>
    </Layout>
  );
};

export default FlowerAI;
