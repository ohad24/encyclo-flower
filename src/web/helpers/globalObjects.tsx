import { IPlantDetails } from "./interfaces";

export const globalColors = [
  { id: 1, color: "#008000", name: "ירוק", isActive: false },
  { id: 2, color: "#660022", name: "בורדו", isActive: false },
  { id: 3, color: "##ffb3cc", name: "ורוד", isActive: false },
  { id: 4, color: "#cce6ff", name: "תכלת", isActive: false },
  { id: 5, color: "#f2f2f2", name: "לבן", isActive: false },
  { id: 6, color: "#9900cc", name: "סגול", isActive: false },
  { id: 7, color: "#c20a38", name: "אדום", isActive: false },
  { id: 8, color: "#fbd9b6", name: "קרם", isActive: false },
  { id: 9, color: "#cccc00", name: "צהוב", isActive: false },
  { id: 10, color: "#664400", name: "חום", isActive: false },
  { id: 11, color: "#333333", name: "שחור", isActive: false },
  { id: 12, color: "#c2660a", name: "כתום", isActive: false },
  { id: 13, color: "#1a8cff", name: "כחול", isActive: false },
];

export const globalTaxon: IPlantDetails["taxon"] = {
  genus: "סוג",
  subfamily: "תת-משפחה",
  family: "משפחה",
  clade4: "סדרה",
  clade3: "מחלקה",
  clade2: "מערכה",
  clade1: "מערכת על",
};

export const monthsText = [
  { name: "ינואר", isActive: false },
  { name: "פברואר", isActive: false },
  { name: "מרץ", isActive: false },
  { name: "אפריל", isActive: false },
  { name: "מאי", isActive: false },
  { name: "יוני", isActive: false },
  { name: "יולי", isActive: false },
  { name: "אוגוסט", isActive: false },
  { name: "ספטמבר", isActive: false },
  { name: "אוקטובר", isActive: false },
  { name: "נובמבר", isActive: false },
  { name: "דצמבר", isActive: false },
];
