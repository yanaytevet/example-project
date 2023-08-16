export const matSortingDataAccessor = (obj: any, property: string) => {
  if (property.indexOf('.') !== -1) {
    const propertyArr: string[] = property.split('.');
    propertyArr.forEach(key => {
      if (obj) {
        obj = obj[key];
      }
    });
    return obj;
  } else {
    return obj[property];
  }
};
