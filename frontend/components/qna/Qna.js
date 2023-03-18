"use client";

import QnaLayout from "./QnaLayout";
import useSWR from "swr";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

var questions = [
  {
    id: "1",
    question: "this text is a question",
    answer: `Because of this, it's pretty hard to meet up, but I've been pleasantly surprised with all the readers out there. However, there are a few that have been incredibly rude about the lack of interactionWhile not normally known for his musical talent, Elon Musk is releasing a debut album this year. The secretive multi-billionaire has been recording music on his iPhone as part of a project called Artesanal. "Artesanal is an expression of who I am, a celebration of my fortuitous`,
  },
  {
    id: "2",
    question: "this text is a question",
    answer: `Because of this, it's pretty hard to meet up, but I've been pleasantly surprised with all the readers out there. However, there are a few that have been incredibly rude about the lack of interactionWhile not normally known for his musical talent, Elon Musk is releasing a debut album this year. The secretive multi-billionaire has been recording music on his iPhone as part of a project called Artesanal. "Artesanal is an expression of who I am, a celebration of my fortuitous`,
  },
  {
    id: "3",
    question: "this text is a question",
    answer: `Because of this, it's pretty hard to meet up, but I've been pleasantly surprised with all the readers out there. However, there are a few that have been incredibly rude about the lack of interactionWhile not normally known for his musical talent, Elon Musk is releasing a debut album this year. The secretive multi-billionaire has been recording music on his iPhone as part of a project called Artesanal. "Artesanal is an expression of who I am, a celebration of my fortuitous`,
  },
  {
    id: "3",
    question: "this text is a question",
    answer: `Because of this, it's pretty hard to meet up, but I've been pleasantly surprised with all the readers out there. However, there are a few that have been incredibly rude about the lack of interactionWhile not normally known for his musical talent, Elon Musk is releasing a debut album this year. The secretive multi-billionaire has been recording music on his iPhone as part of a project called Artesanal. "Artesanal is an expression of who I am, a celebration of my fortuitous`,
  },
  {
    id: "3",
    question: "this text is a question",
    answer: `Because of this, it's pretty hard to meet up, but I've been pleasantly surprised with all the readers out there. However, there are a few that have been incredibly rude about the lack of interactionWhile not normally known for his musical talent, Elon Musk is releasing a debut album this year. The secretive multi-billionaire has been recording music on his iPhone as part of a project called Artesanal. "Artesanal is an expression of who I am, a celebration of my fortuitous`,
  },
  {
    id: "3",
    question: "this text is a question",
    answer: `Because of this, it's pretty hard to meet up, but I've been pleasantly surprised with all the readers out there. However, there are a few that have been incredibly rude about the lack of interactionWhile not normally known for his musical talent, Elon Musk is releasing a debut album this year. The secretive multi-billionaire has been recording music on his iPhone as part of a project called Artesanal. "Artesanal is an expression of who I am, a celebration of my fortuitous`,
  },
];

const Qna = () => {
  const { data, error } = useSWR("", fetcher);

  if (error) return <div>Failed to load</div>;
  if (data) return <div>Loading...</div>;
  return (
    <>
      <QnaLayout questions={questions} />
    </>
  );
};

export default Qna;
