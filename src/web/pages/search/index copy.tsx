import React, { useEffect, useState } from "react";
import Layout from "components/Layout/Layout";
import { Radio, RadioGroup } from "@chakra-ui/react";

// Custom components
import EnvTypes from "components/Search/EnvTypes";
import FlowersMonths from "components/Search/FlowersMonths";
import FlowerColors from "components/Search/FlowerColors";

// Images
import FlowerShape from "components/FlowerShape/FlowerShape";
import { Input } from "@chakra-ui/react";
import MultipleChoice from "components/Search/MultipleChoice";
import { removeEmptyValues } from "helpers/generics";
import { globalColors, monthsText } from "helpers/globalObjects";
import {
  leafArrangements,
  leafEdges,
  leafShapes,
  stemShapes,
} from "helpers/flowersShapeObjects";

const locations = [
  { name: "חוף הגליל", isActive: false },
  { name: "חוף הכרמל", isActive: false },
  { name: "שרון", isActive: false },
  { name: "מישור החוף הדרומי", isActive: false },
  { name: "גליל עליון", isActive: false },
  { name: "גליל תחתון", isActive: false },
  { name: "כרמל", isActive: false },
  { name: "רמות מנשה", isActive: false },
  { name: "עמק יזרעאל", isActive: false },
  { name: "הרי שומרון", isActive: false },
  { name: "שפלת יהודה", isActive: false },
  { name: "הרי יהודה", isActive: false },
  { name: "צפון הנגב", isActive: false },
  { name: "מערב הנגב", isActive: false },
  { name: "מרכז והר הנגב", isActive: false },
  { name: "דרום הנגב", isActive: false },
  { name: "עמק החולה", isActive: false },
  { name: "בקעת כינרות", isActive: false },
  { name: "עמק בית שאן", isActive: false },
  { name: "גלבוע", isActive: false },
  { name: "מדבר שומרון", isActive: false },
  { name: "מדבר יהודה", isActive: false },
  { name: "בקעת הירדן", isActive: false },
  { name: "בקעת ים המלח", isActive: false },
  { name: "ערבה", isActive: false },
  { name: "חרמון", isActive: false },
  { name: "גולן", isActive: false },
];

const lifeForm = [
  { name: "חד-שנתי", isActive: false },
  { name: "גיאופיט (בצל או פקעת)", isActive: false },
  { name: "עשבוני רב-שנתי", isActive: false },
  { name: "שיח", isActive: false },
  { name: "בן-שיח", isActive: false },
  { name: "מטפס", isActive: false },
  { name: "עץ", isActive: false },
  { name: "צמח מים", isActive: false },
  { name: "טפיל", isActive: false },
  { name: "שרכים", isActive: false },
  { name: "דו-שנתי", isActive: false },
  { name: "טחבים", isActive: false },
];

const growAreas = [
  { name: "חולות", isActive: false },
  { name: "קרקעות קלות", isActive: false },
  { name: "בתות", isActive: false },
  { name: "בתות של הרים גבוהים", isActive: false },
  { name: "חברות שיחים", isActive: false },
  { name: "ערבות-שיחים", isActive: false },
  { name: "קרקעות כבדות", isActive: false },
  { name: "בתי גידול לחים", isActive: false },
  { name: "מדבר", isActive: false },
  { name: "מחשופי סלע קשה", isActive: false },
  { name: "קירות וחומות", isActive: false },
  { name: "סביבות חמות - צמחים אוהבי חום", isActive: false },
  { name: "קרקעות מלוחות", isActive: false },
  { name: "חורש", isActive: false },
  { name: "בתה עשבונית ים-תיכונית", isActive: false },
  { name: "נטע אדם", isActive: false },
  { name: "שטחים מופרים", isActive: false },
  { name: "שדות ושטחים מעובדים", isActive: false },
  { name: "יער", isActive: false },
  { name: "חוף הים התיכון", isActive: false },
  { name: "קרקעות עשירות בנוטריינטים", isActive: false },
  { name: "מחשופי סלע מוצלים", isActive: false },
  { name: "יער ספר הררי", isActive: false },
];

const leafShapeList = [
  { name: "עגול", isActive: false },
  { name: "מצולע", isActive: false },
  { name: "חסר גבעול", isActive: false },
  { name: "מרובע", isActive: false },
  { name: "משולש", isActive: false },
];

const kozim = [
  { name: "ענפים", isActive: false },
  { name: "עלים", isActive: false },
  { name: "גבעולים", isActive: false },
  { name: "פירות", isActive: false },
  { name: "פרחים", isActive: false },
];

import Loader from "components/Loader/Loader";
import { ISearchResult, IState } from "helpers/interfaces";
import { searchPlant } from "services/flowersService";
import SearchResult from "components/SearchResult/SearchResult";
import SearchResults from "components/SearchResults/SearchResults";
import RotateIcon from "components/Icons/CamaraIcon copy";
import { UpdateResultsByAttributes } from "redux/action";
import { useDispatch } from "react-redux";

// Main component
const Search = () => {
  const [value, setValue] = React.useState<string>("1");
  const [searchResults, setSearchResults] = React.useState<ISearchResult[]>([]);
  const [isNoResults, setNoResults] = React.useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = React.useState<boolean>(false);

  const [state, setState] = useState<IState>({
    name_text: "",
    colors: [],
    location_names: [],
    flowering_seasons: [],
    petals: [],
    leaf_shapes: [],
    leaf_edges: [],
    leaf_arrangements: [],
    life_forms: [],
    habitats: [],
    stem_shapes: [],
    spine: [],
    red: false,
    invasive: false,
    danger: false,
    rare: false,
    protected: false,
    page: 1,
  });

  const onChange = <T,>(name: string, value: T) => {
    setState({ ...state, [name]: value });
  };

  const onMonthChange = (month: string, isIn: boolean) => {
    if (!isIn) {
      setState({
        ...state,
        flowering_seasons: state.flowering_seasons.filter((x) => x !== month),
      });
    } else {
      const months: string[] = [...state.flowering_seasons];
      months.push(month);
      setState({ ...state, flowering_seasons: months });
    }
  };

  const onColorChange = (color: string, isIn: boolean) => {
    if (!isIn) {
      setState({ ...state, colors: state.colors.filter((x) => x !== color) });
    } else {
      const colors: string[] = [...state.colors];
      colors.push(color);
      setState({ ...state, colors: colors });
    }
  };

  const onLocationChanged = (value: string, isIn: boolean) => {
    if (!isIn) {
      setState({
        ...state,
        location_names: state.location_names.filter((x) => x !== value),
      });
    } else {
      const newLocation: string[] = [...state.location_names];
      newLocation.push(value);
      setState({ ...state, location_names: newLocation });
    }
  };

  const onLifeFormChanged = (value: string, isIn: boolean) => {
    if (!isIn) {
      setState({
        ...state,
        life_forms: state.life_forms.filter((x) => x !== value),
      });
    } else {
      const newForm: string[] = [...state.life_forms];
      newForm.push(value);
      setState({ ...state, life_forms: newForm });
    }
  };

  const onHabitatsChanged = (value: string, isIn: boolean) => {
    if (!isIn) {
      setState({
        ...state,
        habitats: state.habitats.filter((x) => x !== value),
      });
    } else {
      const newForm: string[] = [...state.habitats];
      newForm.push(value);
      setState({ ...state, habitats: newForm });
    }
  };

  const onSteamShapeChanged = (value: string, isIn: boolean) => {
    const newForm: string[] = [value];
    setState({ ...state, stem_shapes: newForm });
  };

  const onSpineChanged = (value: string, isIn: boolean) => {
    if (!isIn) {
      setState({ ...state, spine: state.spine.filter((x) => x !== value) });
    } else {
      const newForm: string[] = [...state.spine];
      newForm.push(value);
      setState({ ...state, spine: newForm });
    }
  };

  const onShapeChange = (value: string, isIn: boolean) => {
    if (!isIn) {
      setState({
        ...state,
        leaf_shapes: state.leaf_shapes.filter((x) => x !== value),
      });
    } else {
      const leafShape: string[] = [...state.leaf_shapes];
      leafShape.push(value);
      setState({ ...state, leaf_shapes: leafShape });
    }
  };

  const onArrangementChange = (value: string, isIn: boolean) => {
    if (!isIn) {
      setState({
        ...state,
        leaf_arrangements: state.leaf_arrangements.filter((x) => x !== value),
      });
    } else {
      const leafShape: string[] = [...state.leaf_arrangements];
      leafShape.push(value);
      setState({ ...state, leaf_arrangements: leafShape });
    }
  };

  const onEdgesChange = (value: string, isIn: boolean) => {
    if (!isIn) {
      setState({
        ...state,
        leaf_edges: state.leaf_edges.filter((x) => x !== value),
      });
    } else {
      const leafShape: string[] = [...state.leaf_edges];
      leafShape.push(value);
      setState({ ...state, leaf_edges: leafShape });
    }
  };

  const onStemsChange = (value: string, isIn: boolean) => {
    if (!isIn) {
      setState({
        ...state,
        stem_shapes: state.stem_shapes.filter((x) => x !== value),
      });
    } else {
      const stemShape: string[] = [...state.stem_shapes];
      stemShape.push(value);
      setState({ ...state, stem_shapes: stemShape });
    }
  };

  const onPetalsChange = (value: string) => {
    setValue(value);
    const arr = [];
    arr.push(value);
    setState({ ...state, petals: arr });
  };

  const dispatch = useDispatch();
  const submitForm = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSearchResults([]);
      setIsSubmitting(true);
      setNoResults(false);
      const values = removeEmptyValues(state);
      const { data } = await searchPlant("plants/search", values);
      setIsSubmitting(false);
      dispatch(UpdateResultsByAttributes(data.results));
      setSearchResults(data.plants);
    } catch (err: any) {
      const error = err;
      console.log("error", error);
      setNoResults(true);
      setIsSubmitting(false);
    }
  };

  const resetAttribute = (arr: any) => {
    arr.map((item: { name: string; isActive: boolean }) => {
      item.isActive = false;
    });
  };

  const resetAll = () => {
    resetAttribute(locations);
    resetAttribute(lifeForm);
    resetAttribute(growAreas);
    resetAttribute(leafShapeList);
    resetAttribute(kozim);
    resetAttribute(globalColors);
    resetAttribute(monthsText);
    resetAttribute(leafArrangements);
    resetAttribute(leafEdges);
    resetAttribute(leafShapes);
    resetAttribute(stemShapes);
    setValue("רבים");
    setState({
      name_text: "",
      colors: [],
      location_names: [],
      flowering_seasons: [],
      petals: [],
      leaf_shapes: [],
      leaf_edges: [],
      leaf_arrangements: [],
      life_forms: [],
      habitats: [],
      stem_shapes: [],
      spine: [],
      red: false,
      invasive: false,
      danger: false,
      rare: false,
      protected: false,
      page: 1,
    });
  };

  useEffect(() => {
    console.log("no result", isNoResults);
  }, [isNoResults]);

  return (
    <Layout>
      <>
        <Loader text="טוען תוצאות חיפוש..." isLoading={isSubmitting} />

        <div className="default-container">
          <form
            onSubmit={(e) => submitForm(e)}
            onKeyDown={(e) => (e.key === "Enter" ? submitForm(e) : "")}
            className="flex flex-col justify-center items-center"
          >
            <div className="flex items-center justify-center my-5">
              <p className="font-bold text-secondary  border-b-4  border-b-primary mb-7 text-2xl  max-w-[320px] text-center ">
                חיפוש צמח לפי מאפיינים
              </p>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-[90%] md:w-[50%]">
                <p className="text-secondary mb-2 font-bold text-md">
                  חיפוש לפי שם צמח
                </p>
                <div className="w-full">
                  <Input
                    placeholder="הקלד שם צמח"
                    value={state.name_text}
                    onChange={(e) => {
                      onChange("name_text", e.target.value);
                    }}
                  />
                </div>
              </div>
              {/* main container */}
              <div className="flex flex-col md:gap-5  md:flex-row mt-5 w-full ">
                <div className="grow-1">
                  <div className="flex flex-col items-center justify-center my-5">
                    <p className="font-bold text-secondary  border-b-4 border-b-primary mb-5 text-md  text-center  md:max-w-[60%] ">
                      שמירת טבע
                    </p>
                    <div>
                      <EnvTypes state={state} onChange={onChange} />
                    </div>
                    <p
                      className="font-bold text-secondary text-center  border-b-4 border-b-primary mb-2 text-md   
										"
                    >
                      מיקום
                    </p>
                    <MultipleChoice
                      list={locations}
                      onChange={onLocationChanged}
                    />

                    <div className="w-full text-center">
                      <p
                        className="font-bold text-secondary text-center max-w-[80px] m-auto border-b-4 border-b-primary mb-2 text-md   
										"
                      >
                        צורות חיים
                      </p>
                      <MultipleChoice
                        list={lifeForm}
                        onChange={onLifeFormChanged}
                      />
                      <p
                        className="font-bold text-secondary text-center max-w-[90px] m-auto border-b-4 border-b-primary my-2 text-md   
										"
                      >
                        צורות גבעול
                      </p>
                      <MultipleChoice
                        list={leafShapeList}
                        onChange={onSteamShapeChanged}
                        isSingSelection={true}
                      />
                      <p
                        className="font-bold text-secondary text-center max-w-[50px] m-auto border-b-4 border-b-primary my-2 text-md   
										"
                      >
                        קוצים
                      </p>
                      <MultipleChoice list={kozim} onChange={onSpineChanged} />
                    </div>
                  </div>
                </div>
                <div className="grow-2 flex flex-col items-center">
                  <div className="flex items-center justify-center my-5 w-full">
                    <p className="font-bold text-secondary max-w-[50px] m-auto border-b-4 border-b-primary text-md  text-center   md:w-[60%]  ">
                      פריחה
                    </p>
                  </div>

                  <FlowersMonths onMonthChange={onMonthChange} />

                  <p className="font-bold text-secondary text-sm text-center md:w-[60%]  md:mt-8 mb-3">
                    צבע פריחה
                  </p>
                  <div className="w-full flex flex-col items-center justify-center">
                    <FlowerColors onColorChange={onColorChange} />
                    <p className="font-bold text-secondary mt-3 mb-2 text-sm  text-center  md:w-[60%] ">
                      מספר עלי כותרת
                    </p>
                    <div className="mb-[10px]">
                      <RadioGroup
                        onChange={onPetalsChange}
                        value={value}
                        className="search-rb"
                      >
                        <div className="flex flex-row  flex-wrap flex-reverse max-w-[195px] gap-3">
                          <div>
                            <Radio size="sm" colorScheme="orange" value="רבים">
                              רבים
                            </Radio>
                          </div>
                          <div>
                            <Radio size="sm" colorScheme="orange" value="3">
                              3
                            </Radio>
                          </div>
                          <div>
                            <Radio size="sm" colorScheme="orange" value="4">
                              4
                            </Radio>
                          </div>
                          <div>
                            <Radio size="sm" colorScheme="orange" value="מאוחה">
                              מאוחה
                            </Radio>
                          </div>
                          <div>
                            <Radio size="sm" colorScheme="orange" value="5">
                              5
                            </Radio>
                          </div>
                          <div>
                            <Radio size="sm" colorScheme="orange" value="6">
                              6
                            </Radio>
                          </div>
                          <div>
                            <Radio
                              size="sm"
                              colorScheme="orange"
                              value="חסר עלי כותרת"
                            >
                              חסר עלי כותרת
                            </Radio>
                          </div>
                        </div>
                      </RadioGroup>
                    </div>
                    <p className="font-bold text-secondary max-w-[70px] m-auto border-b-4 border-b-primary mb-2 text-md  text-center  md:w-[60%] ">
                      בית גידול
                    </p>
                    <MultipleChoice
                      list={growAreas}
                      onChange={onHabitatsChanged}
                    />
                  </div>
                </div>
                <div className="grow-1">
                  <div className="flex flex-col items-center justify-center my-5">
                    <p className="font-bold text-secondary  border-b-4 border-b-primary mb-7 text-md  text-center  ">
                      תכונות ומבנה
                    </p>
                    <p className="font-bold text-secondary    mb-3 text-sm  text-center  ">
                      צורות עלה
                    </p>
                    <FlowerShape
                      startIngIndex={0}
                      onShapeChange={onShapeChange}
                    />
                    <p className="font-bold text-secondary my-3 text-sm  text-center  ">
                      סידור עלים
                    </p>
                    <FlowerShape
                      startIngIndex={4}
                      onShapeChange={onArrangementChange}
                    />

                    <p className="font-bold text-secondary my-3 text-sm  text-center  ">
                      סידור עלים
                    </p>
                    <FlowerShape
                      startIngIndex={5}
                      onShapeChange={onEdgesChange}
                    />

                    <p className="font-bold text-secondary my-3 text-sm  text-center  ">
                      צורת גבעול
                    </p>
                    <FlowerShape
                      startIngIndex={6}
                      onShapeChange={onStemsChange}
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="w-[90%] md:w-[30%] md:hover:w-[30%]  mt-1 md:mt-[3rem] rounded transition-all duration-500">
              <button
                type="submit"
                className="bg-transparent  border-2 border-primary hover:border-transparent  hover:bg-primary text-gray-400 hover:text-white font-bold  p-2 w-full rounded-xl  transition duration-150"
              >
                התחל חיפוש
              </button>
            </div>
            <button
              type="button"
              onClick={resetAll}
              className="flex flex-row bg-transparent max-w-[135px] text-sky-800 font-bold p-0 transition duration-150 m-auto mt-5 mb-10"
            >
              <div
                className="border-2 border-sky-900 rounded-full h-6 w-6 mt-0.5 ml-1"
                style={{ paddingRight: "2.5px", paddingTop: "3px" }}
              >
                <RotateIcon />
              </div>
              <div className="bg-transparent max-w-[135px] text-sky-900 font-bold p-0 transition duration-150 m-auto">
                איפוס נתונים
              </div>
            </button>
            {isNoResults && (
              <div
                className={`mt-4 border-2 border-white border-b-primary
							 text-red-500 text-center w-[30%] p-2 rounded-full font-bold text-sm`}
              >
                לא נמצאו תוצאות חיפוש.
              </div>
            )}
          </form>

          {searchResults.length > 0 ? (
            <SearchResults length={searchResults.length} />
          ) : null}
          {searchResults &&
            searchResults.map((result: any, index: number) => {
              return (
                <SearchResult
                  result={result}
                  index={index}
                  widthButton={109}
                  textButton={"זה הצמח"}
                />
              );
            })}
        </div>
      </>
    </Layout>
  );
};

export default Search;
