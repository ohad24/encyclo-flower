interface Props {
  text: string;
  width: number;
}

const HeadLine = ({ text, width }: Props) => {
  return (
    <div className="flex items-center justify-center my-5">
      <p
        className={`font-bold text-secondary  border-b-4  border-b-primary mb-7 text-2xl  max-w-[${width}px] text-center`}
      >
        {text}
      </p>
    </div>
  );
};

export default HeadLine;
