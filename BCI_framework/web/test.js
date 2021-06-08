// let sequence = [4, 3, 3, 3, 5, 6];
// let gold_standard_1 = [0, 0, 1, 1, 0, 0];
// let user_answer = [0, 1, 1, 0, 1, 0];
// let bigN = 1;

// function getGoldStandard(sequence, bigN) {
//   let len = sequence.length;
//   if (len <= bigN) {
//     console.log("N is too big! NULL returned");
//     return null;
//   }
//   let gold_standard = Array(len).fill(0);
//   for (let i = bigN; i < len; i++) {
//     if (sequence[i - bigN] == sequence[i]) {
//       gold_standard[i] = 1;
//     }
//   }
//   return gold_standard;
// }

// function getAccuracy(sequence_1, sequence_2) {
//   let len1 = sequence_1.length;
//   let len2 = sequence_2.length;
//   if (len1 != len2) {
//     console.log("Lengths are not matched! -1 returned");
//     return -1;
//   }
//   let count = 0;
//   for (let i = 0; i < len1; i++) {
//     if (sequence_1[i] == sequence_2[i]) {
//       count++;
//     }
//   }
//   let accurancy = count / len1;
//   return accuracy;
// }

// let gold_standard = getGoldStandard(sequence, bigN);

// console.log(gold_standard);

// let accurancy = getAccurancy(user_answer, gold_standard);
// console.log(accurancy);

// var dict = {
//   one: [15, 4.5],
//   two: [34, 3.3],
//   three: [67, 5.0],
//   four: [32, 4.1]
// };
// var dictstring = JSON.stringify(dict);
// var fs = require("fs");

// fs.writeFile("thing.json", dictstring, function(err, result) {
//   if (err) console.log("error", err);
// });

// let result = {
//   type: 0,
//   bigN: 1,
//   numberOfElement: 7,
//   keydownSpaceSequence: [1, 2, 3, 3, 4, 5],
// };

// let result_str = JSON.stringify(result);
// console.log(result_str);

console.log(__dirname);
