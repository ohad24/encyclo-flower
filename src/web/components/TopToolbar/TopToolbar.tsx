import Image from "next/image";
import Link from "next/link";
import React from "react";
import glass from "../../images/glass.png";
import link from "../../images/link.png";
import { createObservation } from "services/flowersService";
import { useDispatch, useSelector } from "react-redux";
import { UpdateObservationId } from "redux/action";
import GalleryOrCamera from "components/GalleryOrCamera/GalleryOrCamera";

const TopToolbar = () => {
  const store = useSelector((state: any) => state);
  const dispatch = useDispatch();

  const askTheCommunity = async () => {
    try {
      const data = (
        await createObservation(
          "community/observations/",
          "מהי שאלתך?",
          store.token
        )
      ).data;
      dispatch(UpdateObservationId(data.observation_id));
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="flex flex-col md:flex-row justify-center gap-3 md:gap-10 mt-10">
      <GalleryOrCamera
        isAI={true}
        questionsIds={[]}
        setQuestionsIds={() => {}}
      />
      <div className="toolbar-card">
        <Link href="/search">
          <div className="flex flex-col items-center justify-center p-2">
            <div>
              <Image src={glass} alt="Camara" />
            </div>
            <div className="text-secondary font-bold font-xl">מנוע חיפוש</div>
          </div>
        </Link>
      </div>
      <div className="toolbar-card">
        <Link href="/communitySharing">
          <div
            className="flex flex-col items-center justify-center p-2"
            onClick={askTheCommunity}
          >
            <div>
              <Image src={link} alt="Camara" />
            </div>
            <div className="text-secondary font-bold font-xl">שיתוף </div>
            <div className="text-sm">תצפית\תמונות\פריחה\טיול</div>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default TopToolbar;
