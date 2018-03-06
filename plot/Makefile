.PHONY:  all clean

FIGS_DIR =../figs

DIRS = $(sort $(dir $(wildcard ../data/*/*/)))

all:
	./distribution_prop.py

print-%  : ; @echo $* = $($*)

clean:
	-rm -f ${EPSFIGS}
	-rm -f ${FIGS_DIR}/*.eps
