interface Props {
  icon: JSX.Element;
  text: string;
  funcClick: any;
}

const ButtonAI = ({ icon, text, funcClick }: Props) => {
  return (
    <div
      onClick={funcClick}
      className="cursor-pointer flex justify-center items-center gap-2 text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 min-w-[248px] text-center p-1 rounded shadow hover:shadow-lg"
    >
      {icon}
      <button>{text}</button>
    </div>
  );
};

export default ButtonAI;
