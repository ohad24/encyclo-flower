interface Props {
  length?: number;
}

const SearchResults = ({ length }: Props) => {
  return (
    <div className="flex items-center justify-center my-5">
      <p className="font-bold text-secondary border-b-4 border-b-primary mb-2 text-2xl w-[164px] text-center ">
        תוצאות חיפוש:
      </p>
      <p className="font-bold text-2xl border-b-4 border-b-transparent text-secondary mr-2 mb-2">
        {length}
      </p>
    </div>
  );
};
export default SearchResults;
