/* eslint-disable @next/next/no-img-element */
import React, { useState, useEffect } from "react";
import { IPlantDetails } from "helpers/interfaces";
import Image from "next/image";
import Layout from "components/Layout/Layout";
import { globalTaxon, monthsText } from "helpers/globalObjects";
import { globalColors } from "helpers/globalObjects";
import { useRouter } from "next/router";

import {
  leafArrangements,
  leafEdges,
  leafShapes,
  stemShapes,
} from "helpers/flowersShapeObjects";
import { useSelector } from "react-redux";
import Images from "components/Images/Images";
import { nanoid } from "nanoid";
import HeartIcon from "components/Icons/HeartIcon";
import {
  getWithAuthorization,
  get,
  deleteWithAuthorization,
  putWithAuthorization,
} from "services/flowersService";
import EditIcon from "components/Icons/EditIcon";
import SearchIcon from "components/Icons/SearchIcon";
import RightIcon from "components/Icons/RightIcon";
import Router from "next/router";
import NewSearch from "components/NewSearch/NewSearch";
import Loader from "components/Loader/Loader";
import ModalLoginMessage from "components/Modals/ModalLoginMessage";

const initialState = {
  plant_id: "",
  science_name: "",
  heb_name: "",
  fam_name_eng: null,
  petals: "",
  leaf_shapes: [],
  leaf_edges: [],
  leaf_arrangements: [],
  stem_shapes: "",
  life_forms: [],
  description: "",
  protected: false,
  red: false,
  invasive: false,
  synonym_names_eng: [],
  synonym_names_heb: [],
  locations: [],
  habitats: [],
  flowering_seasons: [],
  colors: [],
  sex_flower: [],
  danger: false,
  rare: false,
  taxon: {
    clade1: "",
    clade2: "",
    clade3: "",
    clade4: "",
    family: "",
    subfamily: "",
    genus: "",
  },
  spine: [],
  images: [],
};

const createArrayString = (arr: string[]): string => {
  return arr.toString();
};

const getColors = (color: string): string => {
  let newColor: string | undefined = globalColors?.find(
    (x) => x.name === color
  )?.color;

  if (newColor === undefined) newColor = "#fff";
  return newColor;
};

const getEnvironmentSavingText = (p: IPlantDetails): string => {
  let text = "";
  if (p.danger) text = "בסכנה";
  if (p.protected) {
    if (text.length > 0) {
      text = text + ", מוגן";
    } else {
      text = text + "מוגן";
    }
  }
  if (p.invasive) {
    if (text.length > 0) {
      text = text + ", פולשני";
    } else {
      text = text + "פולשני";
    }
  }
  if (p.red) {
    if (text.length > 0) {
      text = text + ",אדום";
    } else {
      text = text + "אדום";
    }
  }
  if (p.red) {
    if (text.length > 0) {
      text = text + ",נדיר";
    } else {
      text = text + "נדיר";
    }
  }

  return text.length === 0 ? "-- אין מידע --" : text;
};

const PlanetDetails = () => {
  const router = useRouter();
  const store = useSelector((state: any) => state);
  const [isOpen, setIsOpen] = React.useState(false);
  const [colorHeart, setColorHeart] = useState<string>("#0f4871");
  const [planet, setPlanet] = useState<IPlantDetails>(initialState);
  const [isSubmitting, setIsSubmitting] = React.useState<boolean>(false);

  useEffect(() => {
    async function checkFavorite() {
      try {
        setIsSubmitting(true);
        const dataPlant = (await get(`plants/${router.query.science_name}`))
          .data;
        setPlanet(dataPlant);
        if (store.token) {
          const data = (
            await getWithAuthorization(
              `users/me/favorite-plant/${router.query.science_name}`,
              store.token
            )
          ).data;

          if (data.is_favorite) {
            setColorHeart("orange");
          }
        }
        setIsSubmitting(false);
      } catch (err) {
        console.log(err);
        setIsSubmitting(false);
      }
    }
    checkFavorite();
  }, [router.query.science_name, store.token]);

  const firstMonth: number = planet.flowering_seasons[0] - 1;
  const lastMonth: number =
    planet.flowering_seasons[planet.flowering_seasons.length - 1] - 1;
  const monthsString =
    planet.flowering_seasons.length > 1
      ? `${monthsText[firstMonth].name} - ${monthsText[lastMonth].name}`
      : planet.flowering_seasons.length === 0
      ? "אין"
      : `${monthsText[planet.flowering_seasons[0] - 1].name}`;

  let str_locations = "";
  planet.locations.forEach((location: any) => {
    str_locations += location.location_name + ", ";
  });

  str_locations =
    str_locations.length > 0
      ? str_locations.slice(0, str_locations.length - 2) + "."
      : "אין.";

  planet.stem_shapes = planet.stem_shapes ? planet.stem_shapes : "חסר גבעול";

  const handleClick = async () => {
    try {
      if (colorHeart === "orange") {
        await deleteWithAuthorization(
          `plants/${planet.science_name}/remove-favorite`,
          store.token
        );
        setColorHeart("#0f4871");
      } else {
        await putWithAuthorization(
          `plants/${planet.science_name}/add-favorite`,
          {},
          store.token
        );
        setColorHeart("orange");
      }
    } catch (err) {
      console.log(err);
    }
  };

  const nextPage = (path: string) => {
    Router.push({
      pathname: path,
    });
  };

  return (
    <Layout>
      <div className="default-container lg:px-2">
        <div className="flex justify-center mt-5 md:mt-20">
          <p className="font-bold text-secondary border-b-4 border-b-orange-300 mb-9 text-2xl ml-5">
            {planet.heb_name}
          </p>
          <button
            className="right-11 mb-9"
            onClick={store.token ? handleClick : () => setIsOpen(true)}
          >
            <HeartIcon color={colorHeart} size={25} />
          </button>
        </div>
        <div className="flex flex-col flex-wrap gap-3">
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">משפחה</div>
            <div>{planet.taxon.family}</div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">שם לטיני</div>
            <div>{planet.science_name}</div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">צורות חיים</div>
            <div>
              {planet.life_forms.length > 0
                ? createArrayString(planet.life_forms)
                : "אין"}
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">בית גידול עיקרי</div>
            <div>
              {planet.habitats.length > 0
                ? createArrayString(planet.habitats)
                : "אין"}
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">חודשי פריחה</div>
            <div>{monthsString}</div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">צבעי פרח</div>
            <div>
              <div className="flex flex-wrap gap-1 ">
                {planet.colors?.map((color) => {
                  const bgColor = getColors(color);
                  return (
                    <div
                      key={color}
                      className={`rounded-full w-[14px] h-[14px] border border-gray-700 '`}
                      style={{ backgroundColor: `${bgColor}` }}
                    >
                      &nbsp;
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">מספר עלה כותרת</div>
            <div>{planet.petals}</div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">קוצניות</div>
            <div>
              {planet.spine.length > 0
                ? createArrayString(planet.spine)
                : "ללא קוצים"}
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">שמירת טבע</div>
            <div>{getEnvironmentSavingText(planet)}</div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">שמות נרדפים</div>
            <div>
              {planet.synonym_names_heb.length > 0
                ? createArrayString(planet.synonym_names_heb)
                : "אין"}
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-2 sm:gap-10 text-secondary">
            <div className="font-bold min-w-[8.6rem]">אזורים</div>
            <div>{str_locations}</div>
          </div>
          <div className="flex flex-wrap items-center text-secondary ">
            {Object.keys(planet.taxon).map((key: string, index: number) => {
              const k = key as keyof typeof planet.taxon;
              if (planet.taxon[k] !== null) {
                return (
                  <div key={key} className="relative flex flex-col">
                    <p className="font-bold m-auto">{globalTaxon[k]}</p>
                    <div className="relative flex flex-row">
                      {index !== 0 ? (
                        <div
                          className="absolute border-solid border-t-8 border-r-18"
                          style={{
                            top: "35%",
                            borderWidth: "10px 18px 10px 0",
                            borderColor:
                              "transparent white transparent transparent",
                          }}
                        ></div>
                      ) : null}
                      <div
                        className="w-[126px] h-[70px] text-center pt-4 rounded-2xl"
                        style={{
                          backgroundColor: "#e5dfe1",
                          border: "4px solid #ffffff",
                        }}
                      >
                        {planet.taxon[k]}
                      </div>
                      {index + 1 !== Object.keys(planet.taxon).length ? (
                        <div
                          className="absolute border-solid z-10"
                          style={{
                            borderWidth: "20px 30px 20px 0",
                            borderColor:
                              "transparent #e5dfe1 transparent transparent",
                            right: "85%",
                            top: "20%",
                          }}
                        ></div>
                      ) : null}
                    </div>
                  </div>
                );
              }
            })}
          </div>
        </div>

        <div className="flex flex-wrap">
          <div className="w-[100%] mt-5">
            <Images
              plantName={planet.heb_name}
              photos={planet.images}
              width={500}
              imageFromTheUser={false}
            />
          </div>
        </div>

        <main className="mt-[2rem] text-secondary">
          <div>
            <div className="flex justify-center mt-5">
              <p className="font-bold text-secondary  border-b-4 border-b-orange-300 mb-9 text-2xl ">
                עלים
              </p>
            </div>
            <div className="flex flex-row flex-wrap m-auto w-[100%] items-center">
              <div className="flex flex-row flex-wrap m-auto gap-10">
                <div className="flex flex-col items-center gap-2 font-bold justify-center mb-6 m-auto">
                  <p>צורה</p>
                  <div className="flex flex-wrap justify-center gap-2 min-w-[120px]">
                    {leafShapes
                      .filter((shape) =>
                        planet.leaf_shapes.includes(shape.name)
                      )
                      .map((shape) => {
                        return (
                          <div
                            key={shape.name}
                            className="border-primary border-2 p-[3px] rounded-xl cursor-pointer transition duration-300"
                          >
                            <Image
                              src={shape.image}
                              objectFit="contain"
                              width={50}
                              height={50}
                              alt="Map Image"
                            />
                          </div>
                        );
                      })}
                  </div>
                </div>
                <div className="flex flex-col items-center gap-2 font-bold justify-center mb-6 m-auto">
                  <p>שפה</p>
                  <div className="flex flex-wrap justify-center gap-2  min-w-[120px]">
                    {leafEdges
                      .filter((shape) => planet.leaf_edges.includes(shape.name))
                      .map((shape) => {
                        return (
                          <div
                            key={shape.name}
                            className="border-primary border-2 p-[3px] rounded-xl cursor-pointer transition duration-300"
                          >
                            <Image
                              src={shape.image}
                              objectFit="contain"
                              width={50}
                              height={50}
                              alt="Map Image"
                            />
                          </div>
                        );
                      })}
                  </div>
                </div>
                <div className="flex flex-col items-center gap-2 font-bold justify-center mb-6 m-auto">
                  <p>סידור</p>
                  <div className="flex flex-wrap justify-center gap-2 min-w-[120px]">
                    {leafArrangements
                      .filter((shape) =>
                        planet.leaf_arrangements.includes(shape.name)
                      )
                      .map((shape) => {
                        return (
                          <div
                            key={shape.name}
                            className="border-primary border-2 p-[3px] rounded-xl cursor-pointer transition duration-300"
                          >
                            <Image
                              src={shape.image}
                              objectFit="contain"
                              width={50}
                              height={50}
                              alt="Map Image"
                            />
                          </div>
                        );
                      })}
                  </div>
                </div>
                <div className="flex flex-col items-center gap-2 font-bold justify-center mb-6 m-auto">
                  <p>גבעול</p>
                  <div className="flex flex-wrap justify-center gap-2 min-w-[120px]">
                    {stemShapes
                      .filter((shape) =>
                        planet.stem_shapes?.includes(shape.name)
                      )
                      .map((shape) => {
                        return (
                          <div
                            key={shape.name}
                            className="border-primary border-2 p-[3px] rounded-xl cursor-pointer transition duration-300"
                          >
                            <Image
                              src={shape.image}
                              objectFit="contain"
                              width={50}
                              height={50}
                              alt="Map Image"
                            />
                          </div>
                        );
                      })}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div>
            <div className="flex justify-center mt-5">
              <p className="font-bold text-secondary border-b-4 border-b-orange-300 mb-9 text-2xl ">
                חודשי פריחה
              </p>
            </div>
            <div className="flex justify-center gap-2 ">
              <div className="flex justify-center gap-2 flex-wrap w-[100%] ">
                {monthsText.map((month, index) => {
                  return (
                    <div
                      key={month.name}
                      className={`border p-3 rounded-xl text-xs 
											 ${
                         planet.flowering_seasons.includes(index + 1)
                           ? "bg-primary text-white"
                           : "border-secondary"
                       }
											 w-[72px] text-center`}
                    >
                      <div className="flex flex-col  justify-center items-center">
                        <div>{month.name}</div>
                        <div className="font-bold">{index + 1}</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
          <article className="whitespace-pre-wrap mt-10">
            {planet.description?.split("\n").map((row) => {
              if (row[0] === "@") {
                return (
                  <div key={nanoid()} className="flex justify-center mt-5">
                    <p className="font-bold text-secondary border-b-4 border-b-orange-300 mb-9 text-2xl ">
                      {row.slice(2)}
                    </p>
                  </div>
                );
              }
              return <div key={nanoid()}>{row}</div>;
            })}
          </article>
        </main>
        <button className="flex flex-row-reverse text-base m-auto text-orange-400 h-[25px] w-[103px] mt-5">
          עריכת צמח{" "}
          <div className="mt-1 ml-1">
            <EditIcon color={"#fb923c"} />
          </div>
        </button>
        <div className="flex flex-row flex-wrap sm:flex-nowrap w-[120px] sm:w-[395px] m-auto">
          <button
            onClick={() => nextPage("/search")}
            className="flex flex-col-reverse text-base m-auto text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 h-[100px] w-[120px] mt-2 sm:mt-5 rounded-3xl"
          >
            <span className="table m-auto">
              <span className="table m-auto">
                <SearchIcon size={22} />
              </span>
              <span className="flex flex-col break-normal leading-5 max-w-[42px] font-bold">
                חיפוש חדש
              </span>
            </span>
          </button>
          <NewSearch
            isSearchFromPlant={true}
            isAI={true}
            questionsIds={[]}
            setQuestionsIds={() => {}}
          />
          <button
            onClick={() => nextPage(store.pathname)}
            className="flex flex-col-reverse text-base m-auto text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 h-[100px] w-[120px] mt-2 sm:mt-5 rounded-3xl"
          >
            <span className="table m-auto">
              <span className="table m-auto">
                <RightIcon size={22} />
              </span>
              <span className="flex flex-wrap break-normal leading-5 max-w-[120px] font-bold">
                חזרה לתוצאות החיפוש
              </span>
            </span>
          </button>
        </div>
        <Loader text="טוען נתונים..." isLoading={isSubmitting} />
        <ModalLoginMessage isOpen={isOpen} setIsOpen={setIsOpen} />
      </div>
    </Layout>
  );
};

export default PlanetDetails;
