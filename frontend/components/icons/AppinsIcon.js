import Image from "next/image";

export default function AppinsIcon() {
  return (
    <Image
      src={require("../../public/mark.svg")}
      width={24}
      height={24}
      alt="home page link"
    />
  );
}
