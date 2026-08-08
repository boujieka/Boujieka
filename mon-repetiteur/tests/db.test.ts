import { afterAll, describe, expect, it } from "vitest";
import { prisma } from "@/lib/prisma";

// Integration test against a real Postgres database (see .env / CI's
// postgres service). Exercises the core relation chain — Subject →
// CurriculumTopic → Exercise — and confirms cascading deletes work as
// the schema declares them.
describe("database schema", () => {
  const slug = `test-subject-${Date.now()}`;

  afterAll(async () => {
    await prisma.subject.deleteMany({ where: { slug } });
    await prisma.$disconnect();
  });

  it("writes and reads through the Subject → Topic → Exercise chain", async () => {
    const subject = await prisma.subject.create({
      data: { slug, name: "Test Subject" },
    });

    const topic = await prisma.curriculumTopic.create({
      data: {
        subjectId: subject.id,
        level: "SIXIEME",
        title: "Test topic",
      },
    });

    const exercise = await prisma.exercise.create({
      data: {
        topicId: topic.id,
        type: "MULTIPLE_CHOICE",
        prompt: "2 + 2 = ?",
        content: { choices: ["3", "4", "5"], correctIndex: 1 },
      },
    });

    const found = await prisma.subject.findUniqueOrThrow({
      where: { id: subject.id },
      include: { topics: { include: { exercises: true } } },
    });

    expect(found.topics).toHaveLength(1);
    expect(found.topics[0].exercises).toHaveLength(1);
    expect(found.topics[0].exercises[0].id).toBe(exercise.id);
  });

  it("cascades deletes from Subject down to Topic and Exercise", async () => {
    const subject = await prisma.subject.create({
      data: { slug: `${slug}-cascade`, name: "Cascade Test Subject" },
    });
    const topic = await prisma.curriculumTopic.create({
      data: { subjectId: subject.id, level: "TERMINALE", title: "Cascade topic" },
    });
    await prisma.exercise.create({
      data: {
        topicId: topic.id,
        type: "TRUE_FALSE",
        prompt: "Paris is the capital of France.",
        content: { answer: true },
      },
    });

    await prisma.subject.delete({ where: { id: subject.id } });

    const remainingTopics = await prisma.curriculumTopic.findMany({
      where: { subjectId: subject.id },
    });
    expect(remainingTopics).toHaveLength(0);
  });

  it("enforces unique mastery per user/topic via TopicProgress", async () => {
    const subject = await prisma.subject.create({
      data: { slug: `${slug}-progress`, name: "Progress Test Subject" },
    });
    const topic = await prisma.curriculumTopic.create({
      data: { subjectId: subject.id, level: "SECONDE", title: "Progress topic" },
    });
    const user = await prisma.user.create({
      data: { email: `${slug}@example.com`, name: "Test Student" },
    });

    await prisma.topicProgress.create({
      data: { userId: user.id, topicId: topic.id, masteryScore: 0.5 },
    });

    await expect(
      prisma.topicProgress.create({
        data: { userId: user.id, topicId: topic.id, masteryScore: 0.9 },
      }),
    ).rejects.toThrow();

    await prisma.user.delete({ where: { id: user.id } });
    await prisma.subject.delete({ where: { id: subject.id } });
  });
});
