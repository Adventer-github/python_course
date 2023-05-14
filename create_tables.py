def cmd_create_tables():
    return """
    
        CREATE TABLE "employees" (
          "id" SERIAL PRIMARY KEY,
          "fio" TEXT NOT NULL,
          "title" TEXT NOT NULL
        );
        
        CREATE TABLE "groups" (
          "id" SERIAL PRIMARY KEY,
          "group_name" TEXT NOT NULL,
          "count_of_children" INTEGER
        );
        
        CREATE TABLE "children" (
          "id" SERIAL PRIMARY KEY,
          "fio" TEXT NOT NULL,
          "birthdate" DATE,
          "sex" TEXT NOT NULL,
          "groups" INTEGER NOT NULL
        );
        
        CREATE INDEX "idx_children__groups" ON "children" ("groups");
        
        ALTER TABLE "children" ADD CONSTRAINT "fk_children__groups" FOREIGN KEY ("groups") REFERENCES "groups" ("id") ON DELETE CASCADE;
        
        CREATE TABLE "group_employer" (
          "groupss" INTEGER NOT NULL,
          "employeess" INTEGER NOT NULL,
          PRIMARY KEY ("groupss", "employeess")
        );
        
        CREATE INDEX "idx_group_employer__employeess" ON "group_employer" ("employeess");
        
        ALTER TABLE "group_employer" ADD CONSTRAINT "fk_group_employer__employeess" FOREIGN KEY ("employeess") REFERENCES "employees" ("id") ON DELETE CASCADE;
        
        ALTER TABLE "group_employer" ADD CONSTRAINT "fk_group_employer__groupss" FOREIGN KEY ("groupss") REFERENCES "groups" ("id") ON DELETE CASCADE;
        
        CREATE TABLE "walks" (
          "id" SERIAL PRIMARY KEY,
          "date" DATE,
          "time" TEXT NOT NULL,
          "groups" INTEGER NOT NULL
        );
        
        CREATE INDEX "idx_walks__groups" ON "walks" ("groups");
        
        ALTER TABLE "walks" ADD CONSTRAINT "fk_walks__groups" FOREIGN KEY ("groups") REFERENCES "groups" ("id");
        
        CREATE TABLE "wors_sheludes" (
          "id" SERIAL PRIMARY KEY,
          "day" TEXT NOT NULL,
          "room" INTEGER,
          "groups" INTEGER NOT NULL,
          "work_name" TEXT NOT NULL
        );
        
        CREATE INDEX "idx_wors_sheludes__groups" ON "wors_sheludes" ("groups");
        
        ALTER TABLE "wors_sheludes" ADD CONSTRAINT "fk_wors_sheludes__groups" FOREIGN KEY ("groups") REFERENCES "groups" ("id")
    """