import { MigrationInterface, QueryRunner } from "typeorm";

export class AddBirthdayToUser1736423132044 implements MigrationInterface {
    name = 'AddBirthdayToUser1736423132044'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "users" ADD "birthday" date`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "users" DROP COLUMN "birthday"`);
    }

}