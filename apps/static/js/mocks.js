Date = (function (oldDate, oldnow) {
    function Date(year, month, date, hours, minutes, seconds, ms) {
         let numArgs = arguments.length;
         if (numArgs === 0) {
             return new oldDate(Date.now());
         } else if (numArgs === 1) {
             return new oldDate(year); // milliseconds since epoch, actually
         } else {
             return new oldDate(2020, 1, 7);
         }
    }
    Date.prototype = oldDate.prototype; // required for instanceof checks
    Date.now = function() {
         return oldnow();
    };
    Date.parse = oldDate.parse;
    Date.UTC = oldDate.UTC;
    return Date;
})(Date, Date.now);
