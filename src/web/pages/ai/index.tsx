import React from "react";
import Layout from "../../components/Layout/Layout";
import { useSelector } from "react-redux";
import MenuAI from "components/MenuAI/MenuAI";
import ModalDirective from "components/Modals/ModalDirective";
import ImagePlant from "components/ImagePlant/ImagePlant";
import SearchResults from "components/SearchResults/SearchResults";
import SearchResult from "components/SearchResult/SearchResult";

const FlowerAI = () => {
  const [isOpen, setIsOpen] = React.useState(false);
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
          {Array.from(store.selectedImages).map((selectedImage: any, index) => {
            return (
              <ImagePlant
                key={selectedImage.name}
                index={index}
                selectedImage={selectedImage}
              />
            );
          })}
        </div>
        <SearchResults length={store.results.length} />

        {store.results &&
          store.results.map((result: any, index: number) => {
            return (
              <SearchResult
                key={result.science_name}
                result={result}
                index={index}
                widthButton={109}
                textButton={"זה הצמח"}
              />
            );
          })}
      </div>
    </Layout>
  );
};

export default FlowerAI;
