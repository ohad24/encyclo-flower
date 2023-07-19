import EditIcon from "components/Icons/EditIcon";
import FemaleIcon from "components/Icons/FemaleIcon";
import MaleIcon from "components/Icons/MaleIcon";
import Layout from "components/Layout/Layout";
import SearchResult from "components/SearchResult/SearchResult";
import { Select } from "@chakra-ui/react";
import Suggestions from "components/Suggestions/Suggestions";
import { IUser } from "helpers/interfaces";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { getIsFavorite, update } from "services/flowersService";
import Images from "components/Images/Images";
import SaveIcon from "components/Icons/SaveIcon";
import Loader from "components/Loader/Loader";

const initialUser = {
  user_id: "",
  username: "",
  f_name: "",
  l_name: "",
  settlement: "",
  sex: "",
  create_dt: "",
  phone: "",
  email: "",
  observations: [],
  questions: [],
  image_detections: [],
  favorite_plants: [],
};

const MyProfile = () => {
  const [user, setUser] = useState<IUser>(initialUser);
  const [editUser, setEditUser] = useState<IUser>(initialUser);
  const [errors, setErrors] = useState({
    ...editUser,
  });
  const [clickEdit, setClickEdit] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const store = useSelector((state: any) => state);
  useEffect(() => {
    async function getUser() {
      try {
        setIsSubmitting(true);
        const data = (await getIsFavorite("users/me", store.token)).data;
        setUser(data);
        setEditUser(data);
        setIsSubmitting(false);
      } catch (err) {
        console.log(err);
        setIsSubmitting(false);
      }
    }
    getUser();
  }, []);

  const onChange = (
    e: React.FormEvent<HTMLInputElement> | React.ChangeEvent<HTMLSelectElement>
  ) => {
    const name = e.currentTarget.name;
    const value = e.currentTarget.value;
    setEditUser({ ...editUser, [name]: value });
  };

  const isError = (p: string) => {
    const isError: boolean = p.length > 1;
    return isError;
  };

  const isValidEmail = (email: string) => {
    const isValid = /\S+@\S+\.\S+/.test(email);
    return isValid;
  };

  const validateForm = () => {
    let isValid: boolean = true;
    if (editUser.f_name.length < 1) {
      setErrors((prev) => {
        return { ...prev, f_name: "שם פרטי - חובה" };
      });
      isValid = false;
    }

    if (editUser.l_name.length < 1) {
      setErrors((prev) => {
        return { ...prev, l_name: "שם משפחה - חובה" };
      });
      isValid = false;
    }

    if (!isValidEmail(editUser.email)) {
      setErrors((prev) => {
        return { ...prev, email: 'דוא"ל לא תקני' };
      });
      isValid = false;
    }

    if (!editUser.sex || editUser.sex === "0") {
      setErrors((prev) => {
        return { ...prev, sex: "יש לבחור מגדר." };
      });
      isValid = false;
    }
    return isValid;
  };

  const saveDetails = async () => {
    if (!validateForm()) return;
    try {
      await update(`users/${user.username}`, editUser, store.token);
      setUser({ ...user, ...editUser });
      setClickEdit(false);
    } catch (err) {
      console.log(err);
    }
  };

  const cancel = () => {
    setClickEdit(false);
    setEditUser({ ...user });
  };

  return (
    <Layout>
      <div className="default-container">
        <div className="flex flex-col justify-center items-center max-w-[100%] m-auto">
          <div className="flex items-center justify-center my-5 ">
            <p className="font-bold text-secondary border-b-4 border-b-primary text-2xl max-w-[205px] text-center ">
              הפרופיל שלי{" "}
            </p>
          </div>
          <div className="text-xl text-center text-sky-900">
            <div>
              {!clickEdit && (
                <div>
                  <div className="max-w-[65px] m-auto">
                    {user.sex === "זכר" ? (
                      <MaleIcon />
                    ) : user.sex === "נקבה" ? (
                      <FemaleIcon />
                    ) : null}
                  </div>
                  <p className="font-medium">
                    {user.f_name + " " + user.l_name}
                  </p>
                  <p>{user.email}</p>
                  <p>{user.phone}</p>
                  <p>{user.settlement}</p>
                  <p>{user.sex}</p>
                  <div>
                    <button
                      className="flex flex-row-reverse text-base m-auto text-orange-400"
                      onClick={() => setClickEdit(true)}
                    >
                      ערוך פרטים{" "}
                      <div className="mt-1 ml-1">
                        <EditIcon color={"#fb923c"} />
                      </div>
                    </button>
                  </div>
                </div>
              )}
              {clickEdit && (
                <div>
                  <div className="flex flex-col sm:flex-row gap-1 sm:gap-4">
                    <div className="flex flex-col">
                      <p className="text-sm text-secondary font-bold mb-2">
                        שם פרטי
                      </p>
                      <input
                        className="input w-full"
                        name="f_name"
                        value={editUser.f_name}
                        onChange={onChange}
                      />
                      <p
                        className={`${
                          isError(errors.f_name) ? "" : "hidden"
                        } bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
                      >
                        {errors.f_name}
                      </p>
                    </div>
                    <div className="flex flex-col">
                      <p className="text-sm text-secondary font-bold mb-2">
                        שם משפחה
                      </p>
                      <input
                        className="input w-full"
                        name="l_name"
                        value={editUser.l_name}
                        onChange={onChange}
                      />
                      <p
                        className={`${
                          isError(errors.l_name) ? "" : "hidden"
                        } bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
                      >
                        {errors.l_name}
                      </p>
                    </div>
                  </div>

                  <div className="flex flex-col sm:flex-row gap-1 sm:gap-4">
                    <div className="flex flex-col">
                      <p className="text-sm text-secondary font-bold mb-2">
                        איימיל
                      </p>
                      <input
                        className="input w-full"
                        name="email"
                        value={editUser.email}
                        onChange={onChange}
                      />
                      <p
                        className={`${
                          isError(errors.email) ? "" : "hidden"
                        } bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
                      >
                        {errors.email}
                      </p>
                    </div>
                    <div className="flex flex-col">
                      <p className="text-sm text-secondary font-bold mb-2">
                        טלפון&nbsp;
                        <span className="text-xs text-gray-400">
                          (אופציונלי)
                        </span>
                      </p>
                      <input
                        className="input w-full"
                        name="phone"
                        value={editUser.phone}
                        onChange={onChange}
                      />
                    </div>
                  </div>
                  <div className="flex flex-col sm:flex-row gap-1 sm:gap-4">
                    <div className="flex flex-col sm:flex-row   gap-1 sm:gap-4">
                      <div className="flex flex-col">
                        <p className="text-sm text-secondary font-bold mb-2">
                          ישוב&nbsp;
                          <span className="text-xs text-gray-400">
                            (אופציונלי)
                          </span>
                        </p>
                        <input
                          className="input w-full"
                          name="settlement"
                          value={editUser.settlement}
                          onChange={onChange}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-col">
                    <p className="text-sm text-secondary font-bold mb-2">
                      מגדר&nbsp;
                    </p>
                    <Select name="sex" value={editUser.sex} onChange={onChange}>
                      <option value="0">-- בחר מגדר --</option>
                      <option value="זכר">זכר</option>
                      <option value="נקבה">נקבה</option>
                    </Select>
                    <p
                      className={`${
                        isError(errors.sex) ? "" : "hidden"
                      } bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
                    >
                      {errors.sex}
                    </p>
                  </div>
                  <div>
                    <div className="flex flex-row flex-wrap m-auto max-w-[218px]">
                      <button onClick={cancel} className="text-red-600 ml-5">
                        {" "}
                        <span className="text-2xl">x</span> ביטול
                      </button>
                      <div className="mt-2.5 ml-1">
                        <SaveIcon size={19} color="#16a34a" />
                      </div>
                      <button
                        className="text-green-600"
                        onClick={saveDetails}
                        style={{ marginTop: "2.5px", color: "#16a34a" }}
                      >
                        {" "}
                        שמור פרטים
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
          <div className="flex items-center justify-center my-5 ">
            <p className="font-bold text-secondary border-b-4 border-b-primary text-2xl max-w-[255px] text-center ">
              תמונות שהעליתי לזיהוי
            </p>
          </div>
          <Images
            photos={user.image_detections.map((image: any) => image.metadata)}
            username={user.username}
            width={520}
            imageFromTheUser={false}
            isQuestion={false}
            imagesDetections={true}
          />
          <div className="flex items-center justify-center my-5 ">
            <p className="font-bold text-secondary border-b-4 border-b-primary text-2xl max-w-[255px] text-center ">
              שאלות ששאלתי
            </p>
          </div>
          {user.questions.map((question: any) => (
            <Suggestions
              key={question.question_id}
              str={"question_text"}
              question={{ ...question, username: user.username }}
              username={user.username}
              isQuestion={true}
            />
          ))}
          <div className="flex items-center justify-center my-5 ">
            <p className="font-bold text-secondary border-b-4 border-b-primary text-2xl max-w-[255px] text-center ">
              הפוסטים שלי{" "}
            </p>
          </div>
          {user.observations.map((observation: any) => (
            <Suggestions
              key={observation.observation_id}
              str={"observation_text"}
              question={{ ...observation, username: user.username }}
              username={user.username}
              isQuestion={false}
            />
          ))}
        </div>
        <div className="flex items-center justify-center my-5 ">
          <p className="font-bold text-secondary border-b-4 border-b-primary text-2xl max-w-[255px] text-center ">
            צמחים שאהבתי{" "}
          </p>
        </div>
        {user.favorite_plants.map((favorite_plant: any, index: number) => (
          <SearchResult
            key={favorite_plant.plant_id}
            result={favorite_plant}
            index={index}
          />
        ))}
        <Loader text="טוען נתונים..." isLoading={isSubmitting} />
      </div>
    </Layout>
  );
};

export default MyProfile;
