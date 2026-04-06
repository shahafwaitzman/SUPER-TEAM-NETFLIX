// ===== MEMBER LIST =====
const MEMBERS = [
  { name: 'שחף ויצמן', email: 'shahafwai@gmail.com' },
  { name: 'הודיה אוחיון', email: 'hodaya1507ohayon@gmail.com' },
  { name: 'רינת ישראל', email: 'Rinati0010@gmail.com' },
  { name: 'יעל רותם', email: 'ylasko76@gmail.com' },
  { name: 'עדן טיבי תדמור', email: 'Edentibi5@gmail.com' },
  { name: 'ליז מאירוביץ', email: 'Lizmeirovich1@gmail.com' },
  { name: 'רבקה דהן', email: 'Rivkanati@gmail.com' },
  { name: 'פולי מאירוביץ ויצמן', email: 'Polly70meirovich@gmail.com' },
  { name: 'נוגה אזרד', email: 'nogazrad122@gmail.com' },
  { name: 'מישל אסא', email: 'Michellelesdman@gmail.com' },
  { name: 'מלי עטר', email: 'maliat1405@gmail.com' },
  { name: 'דנה צפניה', email: 'zfaniadana@gmail.com' },
  { name: 'גיא אסא', email: 'guyassa6@gmail.com' },
  { name: 'עדי שור', email: 'Adishor2025@gmail.com' }
];

// Check if email is member
function isMember(email) {
  return MEMBERS.some(m => m.email.toLowerCase() === email.toLowerCase());
}

// Get member by email
function getMemberByEmail(email) {
  return MEMBERS.find(m => m.email.toLowerCase() === email.toLowerCase());
}
