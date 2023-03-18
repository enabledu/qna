import React, { useEffect, useState } from "react";
import { Input } from "@mui/material";
import styles from "./ask.module.css";

const MuiTags = (props) => {
  const [tags, setTags] = useState(props.tags);

  useEffect(() => {
    props.getTags(tags);
  }, [tags]);
  return (
    <div className={styles.MuiTags}>
      {tags.map((t, t_key) => {
        return (
          <div
            className={`${styles.MuiTagsItem}`}
            key={t_key}
            style={{ color: "white" }}
          >
            {t}{" "}
            <button
              onClick={() => {
                tags.splice(t_key, 1);
                setTags([...tags]);
              }}
            >
              &times;
            </button>
          </div>
        );
      })}
      <div>
        <Input
          placeholder={"Tags..."}
          disableUnderline={true}
          onKeyUp={(e) => {
            if (e.keyCode === 13 && e.target.value.length > 0) {
              if (!tags.includes(e.target.value)) {
                setTags([...tags, e.target.value]);

                e.target.value = "";
              }
            }
          }}
        />
      </div>{" "}
    </div>
  );
};
MuiTags.defaultProps = {
  tags: [],
};
export default MuiTags;
