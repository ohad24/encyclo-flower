interface Props {
  accept_terms_of_service?: boolean;
  error: boolean;
  onAcceptTerms: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const ApprovalOfTerms = ({
  accept_terms_of_service,
  error,
  onAcceptTerms,
}: Props) => {
  return (
    <>
      <div className="mt-4 flex gap-1 ">
        <input
          type="checkbox"
          name="accept_terms_of_service"
          checked={accept_terms_of_service}
          onChange={onAcceptTerms}
        />
        <p className="text-xs text-secondary">
          אני מאשר\ת את תנאי השימוש באנציקלופרח
        </p>
      </div>
      <p
        className={`${
          !error ? "" : "hidden"
        } w-full  bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
      >
        יש לאשר את תנאי השימוש.
      </p>
    </>
  );
};

export default ApprovalOfTerms;
