import Image from "next/image";
import Link from "next/link";
import React from "react";
import glass from "../../images/glass.png";
import link from "../../images/link.png";
import Router from "next/router";
import { create } from "services/flowersService";
import { useDispatch, useSelector } from "react-redux";
import { UpdateObservationId } from "redux/action";
import GalleryOrCamera from "components/GalleryOrCamera/GalleryOrCamera";
import ModalLoginMessage from "components/Modals/ModalLoginMessage";

const TopToolbar = () => {
  const dispatch = useDispatch();
  const store = useSelector((state: any) => state);
  const [isOpen, setIsOpen] = React.useState(false);

  const askTheCommunity = async () => {
    try {
      const data = (
        await create(
          "community/observations/",
          {
            observation_text: "מהי שאלתך?",
          },
          store.token
        )
      ).data;
      dispatch(UpdateObservationId(data.observation_id));
      Router.push({
        pathname: "/communitySharing",
      });
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
              <Image src={glass} alt="Search" />
            </div>
            <div className="text-secondary font-bold font-xl">מנוע חיפוש</div>
          </div>
        </Link>
      </div>
      <div className="toolbar-card">
        <div
          className="flex flex-col items-center justify-center p-2"
          onClick={store.token ? askTheCommunity : () => setIsOpen(true)}
        >
          <div>
            <Image src={link} alt="Share" />
          </div>
          <div className="text-secondary font-bold font-xl">שיתוף </div>
          <div className="text-sm">תצפית\תמונות\פריחה\טיול</div>
        </div>
      </div>
      <ModalLoginMessage isOpen={isOpen} setIsOpen={setIsOpen} />
    </div>
  );
};

export default TopToolbar;
