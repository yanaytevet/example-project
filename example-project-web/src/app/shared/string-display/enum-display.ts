
export class EnumDisplay {
  data: Record<string, string> = {};

  public get(key: any): string {
    if (key in this.data) {
      return this.data[key];
    }
    return key;
  }

  public getKeys(): string[] {
    return Object.keys(this.data);
  }
}
