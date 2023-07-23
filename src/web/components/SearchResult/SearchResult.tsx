import CheckIcon from "components/Icons/CheckIcon";
import Images from "components/Images/Images";
import Router, { useRouter } from "next/router";
import { useDispatch } from "react-redux";
import { UpdatePathName } from "redux/action";

const SearchResult = (props: {
  result: any;
  index: number;
  widthButton: number;
  textButton: string;
}) => {
  const dispatch = useDispatch();
  const router = useRouter();

  const nextPlantPage = () => {
    dispatch(UpdatePathName(router.pathname));
    Router.push({
      pathname: `/plantes/${props.result.science_name}`,
    });
  };

  return (
    <div className="flex flex-col items-center mt-5 text-secondary m-auto">
      <div className="flex flex-row flex-wrap gap-5 w-[100%] mb-2">
        <div className="flex flex-row gap-1 font-bold">
          <div
            style={{
              color: "orange",
              fontSize: "35px",
              height: "50px",
            }}
          >
            {props.index + 1}.
          </div>
          <div>
            <div
              className="cursor-pointer"
              style={{
                paddingTop: "25px",
                height: "50px",
                margin: "0",
                lineHeight: "18px",
              }}
              onClick={() => nextPlantPage()}
            >
              {props.result.heb_name}
              <div className="text-sm">{props.result.science_name}</div>
            </div>
          </div>
        </div>
        <button
          className={`flex flex-row gap-1 mr-auto font-bold text-white bg-sky-800 rounded-xl w-[${props.widthButton}px]`}
          style={{
            minHeight: "35px",
            textAlign: "center",
            paddingTop: "5px",
            paddingRight: "7.5px",
            paddingLeft: "2px",
            marginTop: "16px",
          }}
          onClick={() => nextPlantPage()}
        >
          <CheckIcon size={23} color={"white"}></CheckIcon>
          {props.textButton}
        </button>
      </div>
      <div className="flex flex-wrap w-[100%]">
        <div className="w-[100%]">
          <Images
            photos={props.result.images}
            imageFromTheUser={false}
            width={500}
            plantName={props.result.heb_name}
          />
        </div>
      </div>
    </div>
  );
};
export default SearchResult;
